## TDD Process

The main aspects of the TDD process:

- Functional tests
- Unit tests
- The unit-test/code cycle
- Refactoring

We write a test. We run the test and see it fail. We write some minimal code to get it a little further. We rerun the test and repeat until it passes. Then, optionally, we might refactor our code, using our tests to make sure we don’t break anything.
![Overall TDD process](./4.3.png)

But how does this apply when we have functional tests and unit tests? Well, you can think of the functional test as being a high-level view of the cycle, where “writing the code” to get the functional tests to pass actually involves using another, smaller TDD cycle which uses unit tests.
![The TDD process with functional and unit tests](./4.4.png)

We write a functional test and see it fail. Then, the process of “writing code” to get it to pass is a mini-TDD cycle of its own: we write one or more unit tests, and go into the unit-test/code cycle until the unit tests pass. Then, we go back to our FT to check that it gets a little further, and we can write a bit more of our application—using more unit tests, and so on.

What about refactoring, in the context of functional tests? Well, that means we use the functional test to check that we’ve preserved the behaviour of our application, but we can change or add and remove unit tests, and use a unit test cycle to actually change the implementation.

The functional tests are the ultimate judge of whether your application works or not. The unit tests are a tool to help you along the way.

This way of looking at things is sometimes called “Double-Loop TDD”.

## collectstatic and Other Static Directories

Django dev server will magically find all your static files inside app folders, and serve them for you. That’s fine during development, but when you’re running on a real web server, you don’t want Django serving your static content— using Python to serve raw files is slow and inefficient, and a web server like Apache or Nginx can do this all for you. You might even decide to upload all your static files to a CDN, instead of hosting them yourself.

For these reasons, you want to be able to gather up all your static files from inside their various app folders, and copy them into a single location, ready for deployment. This is what the **collectstatic** command is for.

The destination, the place where the collected static files go, is defined in _settings.py_ as STATIC_ROOT.

We’ll change its value to a folder just outside our repo— I’m going to make it a folder just next to the main source folder:

```
workspace
│ ├── superlists
│ │ ├── lists
│ │ │ ├── models.py │││
│ │ ├── manage.py
│ │ ├── superlists ││
│ ├── static
│ │ ├── base.css
│ │ ├── etc...
```

The logic is that the static files folder shouldn’t be a part of your repository—we don’t want to put it under source control, because it’s a duplicate of all the files that are inside lists/static.

Here’s a neat way of specifying that folder, making it relative to the location of the project base directory:

        # Static files (CSS, JavaScript, Images)
        # https://docs.djangoproject.com/en/1.11/howto/static-files/

        STATIC_URL = '/static/'
        STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))

Take a look at the top of the settings file, and you’ll see how that BASE_DIR variable is helpfully defined for us, using **file** (which itself is a really, really useful Python built-in).

Anyway, let’s try running collectstatic:

        \$ python manage.py collectstatic
        [...]
        Copying '/.../superlists/lists/static/bootstrap/css/
        bootstrap-theme.css' Copying '/.../superlists/lists/static/
        bootstrap/css/bootstrap.min.css'

        76 static files copied to '/.../static'.

And if we look in ../static, we’ll find all our CSS files:

```
\$ tree ../static/ ../static/
├── admin
│ ├── css
│ │ ├── base.css
[...]
│
├── base.css
└── bootstrap
└── xregexp.min.js
├── css
│ ├── bootstrap.css
│ ├── bootstrap.css.map
│ ├── bootstrap.min.css
│ ├── bootstrap-theme.css
│ ├── bootstrap-theme.css.map
│ └── bootstrap-theme.min.css
├── fonts
│ ├── glyphicons-halflings-regular.eot
│ ├── glyphicons-halflings-regular.svg
│ ├── glyphicons-halflings-regular.ttf
│ ├── glyphicons-halflings-regular.woff
│ └── glyphicons-halflings-regular.woff2
└── js
├── bootstrap.js
├── bootstrap.min.js
└── npm.js
14 directories, 76 files
```

## Server Debugging Tips

Deployments are tricky! If ever things don’t go exactly as expected, here are a few tips and things to look out for:

- I’m sure you already have, but double-check that each file is exactly where it should be and has the right contents—a single stray character can make all the difference.
- Nginx error logs go into /var/log/nginx/error.log.
- You can ask Nginx to “check” its config using the -t flag: nginx -t
- Make sure your browser isn’t caching an out-of-date response. Use Ctrl-Refresh, or start a new private browser window.
- This may be clutching at straws, but I’ve sometimes seen inexplicable behaviour on the server that’s only been resolved when I fully restarted it with a sudo reboot.

If you ever get completely stuck, there’s always the option of blowing away your server and starting again from scratch! It should go faster the second time...

## Test-Driving Server Configuration and Deployment

- Tests take some of the uncertainty out of deployment

  For developers, server administration is always “fun”, by which I mean, a process full of uncertainty and surprises. My aim during this chapter was to show that a functional test suite can take some of the uncertainty out of the process.

- Typical pain points - database, static files, dependencies, custom settings

  The things that you need to keep an eye out for on any deployment include your database configuration, static files, software dependencies, and custom settings that differ between development and production. You’ll need to think through each of these for your own deployments.

- Tests allow us to experiment

  Whenever we make a change to our server configuration, we can rerun the test suite, and be confident that everything works as well as it did before. It allows us to experiment with our setup with less fear.

## More Debugging Tips

- Check the Systemd logs for using sudo journalctl -u gunicorn-superlists-staging.ajprojects.xyz.
- You can ask Systemd to check the validity of your service configuration: systemd-analyze verify /path/to/my.service.
- Remember to restart both services whenever you make changes.
- If you make changes to the Systemd config file, you need to run daemon-reload before systemctl restart to see the effect of your changes.

## Producion-Readiness for Server Deployments

A few things to think about when trying to build a production-ready server environment:

- Don’t use the Django dev server in production

  Something like Gunicorn or uWSGI is a better tool for running Django; they will let you run multiple workers, for example.

- Don’t use Django to serve your static files

  There’s no point in using a Python process to do the simple job of serving static files. Nginx can do it, but so can other web servers like Apache or uWSGI.

- Check your settings.py for dev-only settings
  DEBUG=True and ALLOWED_HOSTS are the two we looked at, but you will probably have others (send emails from the server).

- Security

## Tips on Organising Tests and Refactoring

### Use a tests folder

Just as you use multiple files to hold your application code, you should split your tests out into multiple files.

- For functional tests, group them into tests for a particular feature or user story.
- For unit tests, use a folder called tests, with a \_\_init\_\_.py.
- You probably want a separate test file for each tested source code file. For Django, that’s typically test_models.py, test_views.py, and test_forms.py.
- Have at least a placeholder test for every function and class.

### Don’t forget the “Refactor” in “Red, Green, Refactor”

The whole point of having tests is to allow you to refactor your code! Use them, and make your code (including your tests) as clean as you can.

### Don’t refactor against failing tests

- In general!
- But the FT you’re currently working on doesn’t count.
- You can occasionally put a skip on a test which is testing something you haven’t written yet.
- More commonly, make a note of the refactor you want to do, finish what you’re working on, and do the refactor a little later, when you’re back to a working state.
- Don’t forget to remove any skips before you commit your code! You should always review your diffs line by line to catch things like this.

### Try a generic wait_for helper

Having specific helper methods that do explicit waits is great, and it helps to make your tests readable. But you’ll also often need an ad-hoc one-line assertion or Selenium interaction that you’ll want to add a wait to. self.wait_for does the job well for me, but you might find a slightly different pattern works for you.

## On Database-Layer Validation

I always like to push my validation logic down as low as possible.

### Validation at the database layer is the ultimate guarantee of data integrity

It can ensure that, no matter how complex your code at the layers above gets, you have guarantees at the lowest level that your data is valid and consistent.

### But it comes at the expense of flexibility

This benefit doesn’t come for free! It’s now impossible, even temporarily, to have inconsistent data. Sometimes you might have a good reason for temporarily storing data that breaks the rules rather than storing nothing at all. Perhaps you’re importing data from an external source in several stages, for example.

### And it’s not designed for user-friendliness

Trying to store invalid data will cause a nasty IntegrityError to come back from your database, and possibly the user will see a confusing 500 error page. As we’ll see in later chapters, forms-layer validation is designed with the user in mind, anticipating the kinds of helpful error messages we want to send them.

## Tips

### Thin Views

If you find yourself looking at complex views, and having to write a lot of tests for them, it’s time to start thinking about whether that logic could be moved else‐where:

- possibly to a form, like we’ve done here.
- Another possible place would be a custom method on the model class.
- And once the complexity of the app demands it—out of Django-specific files and into your own classes and functions, that capture your core business logic.

### Each test should test one thing

The heuristic is to be suspicious if there’s more than one assertion in a test. Sometimes two assertions are closely related, so they belong together. But often your first draft of a test ends up testing multiple behaviours, and it’s worth rewriting it as several tests. Helper functions can keep them from getting too bloated.

## JavaScript Testing in the TDD Cycle

You may be wondering how these JavaScript tests fit in with our “double loop” TDD cycle. The answer is that they play exactly the same role as our Python unit tests.

1. Write an FT and see it fail.
2. Figure out what kind of code you need next: Python or JavaScript?
3. Write a unit test in either language, and see it fail.
4. Write some code in either language, and make the test pass.
5. Rinse and repeat.

## Exploratory Coding, Spiking, and De-spiking

### Spiking

Exploratory coding to find out about a new API, or to explore the feasibility of a new solution. Spiking can be done without tests. It’s a good idea to do your spike on a new branch, and go back to master when de-spiking.

### De-spiking

Taking the work from a spike and making it part of the production codebase. The idea is to throw away the old spike code altogether, and start again from scratch, using TDD once again. De-spiked code can often come out looking quite different from the original spike, and usually much nicer.

### Writing your FT against spiked code

Whether or not this is a good idea depends on your circumstances. The reason it can be useful is because it can help you write the FT correctly—figuring out how to test your spike can be just as challenging as the spike itself. On the other hand, it might constrain you towards reimplementing a very similar solution to your spiked one—something to watch out for.

## On Mocking in Python

### Mocking and external dependencies

We use mocking in unit tests when we have an external dependency that we don’t want to actually use in our tests. A mock is used to simulate the third-party API. Whilst it is possible to “roll your own” mocks in Python, a mocking framework like the mock module provides a lot of helpful shortcuts which will make it easier to write (and more importantly, read) your tests.

### Monkeypatching

Replacing an object in a namespace at runtime. We use it in our unit tests to replace a real function which has undesirable side effects with a mock object, using the patch decorator.

### The Mock library

Michael Foord (who used to work for the company that spawned PythonAny‐ where, just before I joined) wrote the excellent “Mock” library that’s now been integrated into the standard library of Python 3. It contains most everything you might need for mocking in Python.

### The patch decorator

unittest.mock provides a function called patch, which can be used to “mock out” any object from the module you’re testing. It’s commonly used as a decorator on a test method, or even at the class level, where it’s applied to all the test methods of that class.

### Mocks can leave you tightly coupled to the implementation

Mocks can leave you tightly coupled to your implementation. For that reason, you shouldn’t use them unless you have a good reason.

### Mocks can save you from duplication in your tests

On the other hand, there’s no point in duplicating all of your tests for a function inside a higher-level piece of code that uses that function. Using a mock in this case reduces duplication.
