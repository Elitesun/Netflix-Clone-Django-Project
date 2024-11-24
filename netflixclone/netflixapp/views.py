from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Profile, Movie
import requests
import logging

# Set up logger for error tracking and debugging
logger = logging.getLogger('django')

class Home(View):
    """
    Landing page view that handles the initial user experience:
    - If user is logged in: Redirects to profile selection
    - If user is not logged in: Shows the main landing page
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('netflixapp:profile-list')
        return render(request, 'index.html')

@method_decorator(login_required, name='dispatch')
class ProfileList(View):
    """
    Displays all profiles associated with the logged-in user.
    Similar to Netflix's "Who's watching?" screen.
    
    Security:
    - Requires user authentication (@login_required)
    - Only shows profiles belonging to the current user
    
    Template: profilelist.html
    Context: 
    - profiles: QuerySet of Profile objects linked to the current user
    """
    def get(self, request, *args, **kwargs):
        profiles = request.user.profiles.all()
        context = {'profiles': profiles}
        return render(request, 'profilelist.html', context)

@method_decorator(login_required, name='dispatch')
class ProfileCreate(View):
    """
    Handles the creation of new user profiles.
    
    Security:
    - Requires user authentication (@login_required)
    - Form validation for profile data
    - Exception handling for creation errors
    
    Methods:
    - GET: Displays the profile creation form
    - POST: Processes form submission and creates profile
    
    Template: profilecreate.html
    Form: ProfileForm for handling profile data
    """
    def get(self, request, *args, **kwargs):
        # Display empty profile creation form
        form = ProfileForm()
        context = {'form': form}
        return render(request, 'profilecreate.html', context)
    
    def post(self, request, *args, **kwargs):
        # Process profile creation form submission
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            try:
                # Create profile and associate with current user
                profile = Profile.objects.create(**form.cleaned_data)
                if profile:
                    request.user.profiles.add(profile)
                    return redirect('netflixapp:profile-list')
            except Exception as e:
                # Log error and add form error message
                logger.error(f"Error creating profile: {str(e)}")
                form.add_error(None, "An error occurred while creating the profile.")
        context = {'form': form}
        return render(request, 'profilecreate.html', context)

@method_decorator(login_required, name='dispatch')
class MovieList(View):
    """
    Displays a list of movies fetched from OMDB API for a specific user profile.
    
    Security:
    - Requires user authentication (@login_required)
    - Validates profile ownership
    - Handles API errors gracefully
    
    API Integration:
    - Fetches movie data from OMDB API
    - Implements 10-second timeout
    - Includes error handling for API failures
    
    Error Handling:
    - Profile validation
    - API request errors
    - Invalid profile access attempts
    - General exception handling
    
    Template: movielist.html
    Context:
    - movies: List of movies from OMDB API
    - profile_id: Current profile's UUID
    - error: Error message (if API request fails)
    """
    def get(self, request, profile_id, *args, **kwargs):
        try:
            # Verify profile exists and belongs to current user
            profile = Profile.objects.get(uuid=profile_id)
            
            if profile not in request.user.profiles.all():
                return redirect('netflixapp:profile-list')
            
            # Fetch movies from OMDB API
            api_key = settings.OMDB_API_KEY
            url = f'http://www.omdbapi.com/?s=movie&apikey={api_key}'
            
            try:
                # Make API request with timeout
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                movies = data.get('Search', [])
                
                context = {'movies': movies, 'profile_id': profile_id}
                return render(request, 'movielist.html', context)
            
            except requests.RequestException as e:
                # Handle API request errors
                logger.error(f"OMDB API error: {str(e)}")
                context = {'error': 'Unable to fetch movies at this time.', 'profile_id': profile_id}
                return render(request, 'movielist.html', context)

        except Profile.DoesNotExist:
            # Handle invalid profile access attempts
            logger.warning(f"Attempted to access non-existent profile: {profile_id}")
            return redirect('netflixapp:profile-list')
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error in MovieList view: {str(e)}")
            return redirect('netflixapp:profile-list')

@method_decorator(login_required, name='dispatch')
class MovieDetail(View):
    """
    Displays detailed information about a specific movie.
    
    Security:
    - Requires user authentication (@login_required)
    - Validates movie existence
    - Logs unauthorized access attempts
    
    Error Handling:
    - Handles non-existent movies
    - Logs access attempts to invalid movies
    - Catches and logs unexpected errors
    
    Template: moviedetail.html
    Context:
    - movie: Movie object with detailed information
    """
    def get(self, request, movie_id, *args, **kwargs):
        try:
            # Fetch movie details by UUID
            movie = Movie.objects.get(uuid=movie_id)
            context = {"movie": movie}
            return render(request, 'moviedetail.html', context)
        except Movie.DoesNotExist:
            # Handle and log invalid movie access attempts
            logger.warning(f"Attempted to access non-existent movie: {movie_id}")
            return redirect('netflixapp:profile-list')
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Error in MovieDetail view: {str(e)}")
            return redirect('netflixapp:profile-list')

@method_decorator(login_required, name='dispatch')
class PlayMovie(View):
    """
    Handles the movie playback functionality.
    
    Security:
    - Requires user authentication (@login_required)
    - Validates movie existence
    - Logs unauthorized access attempts
    
    Features:
    - Retrieves video information for the selected movie
    - Converts video QuerySet to list for template rendering
    
    Error Handling:
    - Handles non-existent movies
    - Logs playback attempts for invalid movies
    - Catches and logs unexpected errors
    
    Template: playmovie.html
    Context:
    - movie: List of video data associated with the movie
    """
    def get(self, request, movie_id, *args, **kwargs):
        try:
            # Fetch movie and its associated video data
            movie = Movie.objects.get(uuid=movie_id)
            movie = movie.video.values()  # Get associated video information
            context = {"movie": list(movie)}
            return render(request, 'playmovie.html', context)
        except Movie.DoesNotExist:
            # Handle and log invalid movie access attempts
            logger.warning(f"Attempted to play non-existent movie: {movie_id}")
            return redirect('netflixapp:profile-list')
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Error in PlayMovie view: {str(e)}")
            return redirect('netflixapp:profile-list')

@csrf_exempt
def debug_settings(request):
    """Debug view to check security settings"""
    security_settings = {
        'SECURE_SSL_REDIRECT': getattr(settings, 'SECURE_SSL_REDIRECT', None),
        'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', None),
        'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', None),
        'DEBUG': getattr(settings, 'DEBUG', None),
    }
    return JsonResponse(security_settings)
