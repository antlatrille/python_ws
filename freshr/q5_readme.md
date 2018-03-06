# Push notification

The script is designed to give the best time to notify a user, based on his last two weeks on the product.
If no data has been found, we use a default value.

We define best as "The moment where the user will interact the most with Freshr".

More interactions means potentially more ads views, which directly translates into a monetary advantage.

This tool spots those high activity periods and looks for the first of the day.
Here the push notification is not to make the user come back. It is rather designed to make him use the app on his most attentive moment.

Usage is simple : 
command line,
> python q5.py -f [filename] [user_id]

It requires the libraries `argparse` and `pandas`
