1. I want to register a user into the system.

http://localhost:8000/api/register/

usong json data for example:
{
  "username": "test",
  "email": "test@example.com",
  "password": "password"
}




2. I want all API’s (except the user registration API) to be protected using Basic Authentication
http://localhost:8000/api/login/
use basic authentication if you use postman (username, password)




3. I will provide you with a JSON file containing a list of movies in my cinema. The list will contain the name and description of each movie. I want you to add these movies to your database when your applications start up. However, there are some missing pieces of information namely: release date, main cast, director, and budget. This information is hosted at: https://cinema.stag.rihal.tech, where the API endpoint is: GET /api/movie/{movie_id}
to get all the movies
http://localhost:8000/api/movies/ 


4. I want to be able to rate a movie from 1 to 10, step of 1.
http://localhost:8000/api/rate-movie/ 
use json to rate specific movie such as:
{
  "movie": 1,
  "rating": 8
}


5. I want an API to return to me the list of all movies in the database. This should return the ID, name, description and average rating (average rating of all users in the system) of each movie. The description should be 100 characters or less. If the description exceeds the max limit of 100 characters truncate with “...” however, the last word must be a full meaningful word. For example, not accepted: “this movie is beauti...”, accepted: “this movie is ...”
http://localhost:8000/api/movies/



6. I want an API to return detailed information about a specific movie given the ID. This API should return the following: id, name, description, release date, main cast, director, budget, budget in English words (i.e. Budget 1.5B to one billion five hundred million), my rating and the average rating (average rating of all users in the system)
http://localhost:8000/api/movie/<int:movie_id>/

in this one i fetched it from external api 

external_api_url = f'https://cinema.stag.rihal.tech/api/movie/{movie_id}'
external_response = requests.get(external_api_url)



7. I want to be able to search for a movie. This API should be able to return a list of movies (id, name, description) based on a search parameter which matches either the name or description.

http://127.0.0.1:8000/api/search/?q=your_search_term


8. I want an API that returns my top 5 rated movies (id, name, rating) in descending order (ordered by the rating)
http://127.0.0.1:8000/api/my-top-rated/



9. I would like a feature called 'Memories' where I can record personal memories related to a movie. These memories would include a title, date, photos and a story. For instance, I would like to include the photos I took the day I watched 'Mad Max' in theaters, along with the date and the story of what my friends and I did that day.

http://127.0.0.1:8000/api/memories/add/

Set the type to form-data in postman.
Add text fields (title, date, story, movie) as key-value pairs.
For photos, use the key photos, set the type to File, and upload your images. If you're uploading multiple photos, add multiple photos keys with different files.


10. I want an API to return all my memories (id, movie id, movie name, title).

http://127.0.0.1:8000/api/memories/

11. I want an API to return a memory (id, movie id, movie name, title, story, time ordered list of photos (id, photo name, photo extension i.e. PNG, size i.e. 3KB, time created)) given its id.


http://127.0.0.1:8000/api/memories/<int:memory_id>/


12. I want an API that returns the memory photo given its id.

http://127.0.0.1:8000/api/photos/<int:photo_id>/


13. I want an API to update a memory. This includes changing the title or/and the story


PATCH http://127.0.0.1:8000/api/memories/update/<int:memory_id>/

example: 

{
  "title": "Updated Title",
  "story": "Updated funny story"
}


14. I want an API to upload more photos to a memory or delete some.

http://127.0.0.1:8000/api/memories/<int:memory_id>/upload-photos/

use form-data:
add photos field and change it to file

to delete:
http://127.0.0.1:8000/api/memories/<int:memory_id>/delete-photos/

15. I want an API to delete a memory.

http://127.0.0.1:8000/api/memories/delete/<int:memory_id>/


16. I want an API that calculates the top 5 used words in all stories in memories across the system. This should ignore stop words (e.g. “and”, “the”, “to” etc...)

http://127.0.0.1:8000/api/memories/top-words/


17. I want an API that extract any links or URLs mentioned in a story given the memory ID

http://127.0.0.1:8000/api/memories/<int:memory_id>/extract-urls/


18. For fun, I would like to add a puzzle where the user enters a scrambled movie name and the system tries to guess the actual movie. Say I enter: “eund”, the system should be able to return a movie (id, name, description) -> e.g. (12 or uuid, “Dune”, “A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.”). Another example: “askldjfhaksdf” the API should return “404 not found”
http://127.0.0.1:8000/api/guess-movie/<str:scrambled_name>/



19. To compare my ratings to the average, return a list of the maximum. Say I have ratings of [{“Dune”, 10}, {“The Hobbit”, 5}, {“The Godfather”, 7}] and the corresponding average ratings [{“Dune”, 7}, {“The Hobbit”, 9}, {“The Godfather”, 10}]. This API should return [{id, “Dune”, 10, true}, {id, “The Hobbit”, 9, false}, {id, “The Godfather”, 10, false}] as you can see, the returned list only includes the maximum ratings in addition to the fact if it was my rating (true) or not (false)


http://127.0.0.1:8000/api/compare-ratings/




extra credits:


1. Dockerize your project using docker and docker compose to run your project.

docker-compose build


docker-compose up



2. Imagine a star system where users can purchase stars to award to movies as a gesture of excellence and appreciation. Construct an API where the user can get the minimum number of stars to award given movies (API should expect a list of movie IDs). Put the ratings in an ordered list (exact order given by the user), stars will be given to these movies based on the following requirements:

Each movie must have at least one star.
Movies with higher ratings get more stars than their neighbours.
Return the minimum number of stars the user needs to have to distribute the stars to the moivies.

http://127.0.0.1:8000/api/compare-ratings/

using json for example:

{
  "movie_ids": [1, 2, 3]
}


NOTE
It's kinda slow because the communication between the app and elephantSQL is slow <3
