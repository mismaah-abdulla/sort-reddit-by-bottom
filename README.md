# sort-reddit-by-bottom
Because Reddit doesn't give an option to sort comments by bottom (lowest score first).

## Instructions
Run the python file (Python 3 is required).

Enter reddit thread url.

Html file with results will open once complete.

## Notes

Not using the api because of authentication.

This does not display child comments.

If there are a lot of comments, reddit doesn't load all of them. When this happens, the script fetches all the "more" comments concurrently.

Adjust number of max workers if you don't want your system slowed down by the threads.

Uncomment line 58-59 to get json file with results.
