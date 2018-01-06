# ThemePlates
A way to search, organize and share recipes as part of a cooking lifestyle.

ThemePlates differs from other recipe sharing sites because it:
- Comprehends recipe instructions
  - Allows searching by cooking technique
  - Skill ratings for recipes
- Gamifies cooking
  - Rewards reputation points for posting images of finished recipes
  - Compete with others
  - High reputation users can confer badges by tasting another user's cooking in person
- Smart recipe suggestions
  - Higher engagement from users will generate superior preference data

In addition, it will support standard CRUD for recipes, posts of cooked recipes, and up/downvoting of both.

## Scrapely
This app would not be possible without using the scrapely library. Every time a new recipe source is added we run the add_scraper.py script as follows:
```
python3 add_scraper.py <training params file> <recipe page url>
```
Training params file needs to follow the format of the json example below:
```
{
  '0': 'heat pan to medium-low and some oil until it sizzles',
  '1': 'crack egg into pan and fry until bottom is opaque',
  '2': 'flip and fry until cooked to desired doneness'
}
```
