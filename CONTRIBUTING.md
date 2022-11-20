# Contributing


Before anything, I'd like to thank you for contributing to this project. No matter how small or big of a contribution you make, you will have an effect on the growth of this project. Open-source only works because of people like you.

### What to do

Before getting your hands dirty, it is important to understand what exactly you want to contribute to.

If you have experienced a bug, incompatibilities, installation issues or documentation inaccuracies, you are more than welcome to [create a new issue](https://github.com/Eastern-Skill7173/kivy-audioplayer/issues/new), right here on github.com!

It doesn't just have to be fixing problems! Even if you don't have an issue, submitting your ideas and ways to improve the project is massively appreciated. The view and perspective you bring to as a user is unmatched!

### What NOT to do

If you are having a question about the usage or if something is unclear, you will get much better and faster results reaching out to sites such as [Stack Overflow](https://stackoverflow.com/) or communities and subreddits like [r/learnpython](https://www.reddit.com/r/learnpython/) or [r/learnprogramming](https://www.reddit.com/r/learnprogramming/)

Following these guidelines ensures the fastest possible outreach and the best solution for all. It also indicates that you respect the time of the development team, so we can get back to you as soon as possible!


# Ground Rules

### Be respectful and embracing

Everyone who is present in the contribution scene must agree to our [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)

Remember to keep an open mind and be welcoming of everyone. Be constructive but not hurtful. Embrace newcomers and be sure to guide them.

### Details are everything but so is modesty

When creating an issue, make sure to provide **RELEVANT** details as much as possible.

Details help narrow down where, why and how the issue has occurred.

Versions of python, kivy and the project itself are of great importance, so is the operating system the code is being run on. Providing the error code and location (the line in which the error occurred) is also mandatory.

If you are providing any other details, make sure that they truly have an effect on the problem at hand.

Giving a [minimal reproducible example (MRE)](https://stackoverflow.com/help/minimal-reproducible-example) where the issue is repeated will highlight the issue and bring it to the center of attention paving the way for the community and developers to jump straight to action!


# NOT WRITTEN BEYOND THIS POINT

### Taking contributions to the next level

If you feel like the issue is something that you can fix yourself, you are more than welcome to contribute actual changes to the codebase yourself.

If the changes are more than a few lines it is far better for both sides that you fork the repo, and create a new branch! This will significantly improve the speed of the contribution!

In order to keep up with convention, try naming your branch something like this:

```
git clone 123-android-player-issue
```

Where the beginning number is the supposed issue number on github you are working on, and the rest describes the problem mentioned within the issue.

So all the steps boil down to:

```
# To cloned the repo do:
git clone https://github.com/Eastern-Skill7173/kivy-audioplayer
# To change into the project directory:
cd kivy-audioplayer/
# To create and switch to a new branch:
git checkout -b 123-android-player-issue
```

Make sure that your code writing style matches the repo's. We use flake8 as our linter, mypy as our static type checker, and sphinx as our documentation generator.

After making the changes make sure to run the **tests** in the `./tests/` folder to see if your changes have broken any portion of the original codebase.

If the new code makes a change to the behavior of the code and the tests should fail, writing new tests is in order. You could do this part yourself or inform us so that we take care, but the acknowledgement is necessary.

### Deep diving into GitHub Issues
When creating a new issue you are greeted with two options:

1. Bug report
2. Feature request

If you are trying to fix and issue with the codebase click on *Bug report*.

There will be some fields for you to complete. The most top field indicates the name of your issue, By default it is just *[BUG]*, the name of your issue comes after this. **DO NOT DELETE THE BUG PREFIX**, it is necessary to depict that this issue is indeed a bug report.

The next field is the most important one. This is the field that describes the issue. There is already a template ready to be filled out by you.

Ask yourself these questions:

1. What python, kivy, and kivy-audioplayer versions were you using?
2. On what operating system and its version did you run into the issue?
3. What exactly did you do?
4. What exactly did you expect to see?
5. And finally what happened instead

These questions will form the framework for a good issue report

Follow the template, providing the required software info, describing the bug, expected behavior etc.

### Our philosophy
The philosophy of kivy-audioplayer is to provide all the utilities of a modern player in one small package that will be available on the most popular operating system and could be easily accessed and maintained through your kivy code

Any ideas that contribute to this philosophy are appreciated

### Code style

The code style follows mostly flake8 standards, with type hinting being mandatory for functions and methods but discouraged for attributes. Mypy checking is optional but all handwritten tests must pass unless they are not supposed to

### Labeling conventions for issues

* Your issue title must be prefixed with [BUG] if it depicts a problem with the code
* Your issue title must be prefixed with [FT-REQ] if it suggests a new feature and change to be applied in the future
* Make sure to follow the templates in each issue type
