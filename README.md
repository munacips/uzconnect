# UZConnect

A Django web app that gives University of Zimbabwe students one place to read campus news, post and follow short "quotes", trade goods and services, and vote in polls.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Architecture & Patterns](#architecture--patterns)
- [Data Models](#data-models)
- [Views / Service Layer](#views--service-layer)
- [Navigation & Routing](#navigation--routing)
- [Admin Panel](#admin-panel)
- [Configuration](#configuration)
- [Getting Started](#getting-started)
- [Backend Requirements (HTTP Endpoints)](#backend-requirements-http-endpoints)
- [Deployment](#deployment)
- [Known Limitations](#known-limitations)

---

## Features

### Accounts & Onboarding
- **Sign up** with username, name, email, password (with confirmation), degree programme and a **required display picture**.
- Only **`@students.uz.ac.zw`** email addresses are accepted.
- A **6-digit confirmation number** is emailed over SMTP and checked on `/community/confirm/`.
- **Login** is only allowed for accounts whose `activated` flag is `True`; logout is available from the top bar.
- Every page except sign-up, login and email confirmation requires login (`@login_required`, redirecting to `/community/login/`).

### News (site home page)
- Chronological feed of campus articles (newest first), each with a feature picture.
- Article detail page with an extra **image gallery**, a **view counter** (incremented on each visit) and **comments**.

### Community (social)
- **Quotes feed** – short text posts (up to 5000 characters). The feed shows quotes from the accounts you follow.
- **Like** quotes and **comment** on them (quote detail page).
- **Student search** by username, first name or last name, with **follow / unfollow** buttons.
- **Course mash** – browse all students registered under a given degree programme.
- **My Account** – your own quotes, goods and services, with delete actions.
- **My Profile** – your profile card (bio, follower/following counts, display picture).
- **User profile** – another student's quotes, services, goods and news articles.

### Editors (accounts with `editor = True`)
- **Publish news articles** (title, body, feature picture).
- **Attach additional pictures** to their own articles.
- Non-editors who open these pages are sent back to the community home.

### Campus Biz (marketplace)
- Separate listings for **services** (`/biz/`) and **goods** (`/biz/goods/`), newest first, each with name search.
- Post a **service** or **product** with an estimated price, phone/WhatsApp number, description and feature picture.
- Detail pages with an attached picture gallery.
- Owners can **edit** (any subset of fields) and **delete** their own listings.

### Polls
- List of polls, poll detail page with its nominees, and a **vote** action.
- Voting is rejected once the poll's `end_date` has passed, and duplicate/illegal votes show a "NOT ALLOWED" message.

---

## Tech Stack

| Concern | Package / Tool | Version |
|---|---|---|
| Language | Python | 3.6 – 3.9 (the range supported by Django 3.0) |
| Web framework | Django | 3.0.4 (the version that generated the project and migrations) |
| Database | SQLite 3 | bundled with Python (`db.sqlite3`) |
| Image uploads | Pillow | not pinned in repo (required by `ImageField`) |
| Timezones | pytz | not pinned in repo (used in `votes/views.py`) |
| Stray imports | SQLAlchemy, attrs | not pinned in repo (`from sqlalchemy import null` in `biz/models.py`, `from attr import field` in `biz/forms.py`) |
| Email | Django SMTP backend + Gmail SMTP | `smtp.gmail.com:587`, TLS |
| Front end | Django templates, hand-written CSS and vanilla JS | no build step |
| Package manifest | none | the repo has no `requirements.txt` |

> `django.conf.urls.url()` is used throughout the URLconfs; it was removed in Django 4.0, so the project needs Django < 4.

---

## Project Structure

```text
uzconnect/
├── manage.py                    # Django CLI entry point
├── db.sqlite3                   # Committed SQLite database (development data)
├── .gitignore                   # Present but empty
│
├── uzconnect/                   # Project package
│   ├── settings.py              # Settings: apps, SQLite, static/media paths, Gmail SMTP
│   ├── urls.py                  # Root URLconf mounting the four apps
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
├── news/                        # Campus news articles (site home page)
│   ├── models.py                # Post, PostImage, PostComment
│   ├── views.py                 # home (feed), details (article + comments + view count)
│   ├── forms.py                 # CommentForm
│   ├── urls.py                  # "" and details/<id>/
│   ├── admin.py                 # Registers Post, PostImage
│   └── templates/news/
│       ├── layout.html          # BASE TEMPLATE: header, nav (desktop + mobile), theme CSS
│       ├── home.html            # Article list
│       └── details.html         # Article page, gallery, comments
│
├── community/                   # Accounts, auth, social features
│   ├── models.py                # Account, Quote, QuoteLike, Comment, DisplayPic + programme choices
│   ├── views.py                 # Auth, feed, follow, search, profiles, editor tools, edit/delete
│   ├── forms.py                 # Login, SignUp, Quote, Article, Comment, Confirm, search, Good/Service edit forms
│   ├── urls.py                  # All /community/ routes
│   ├── gettrending.py           # Stub module (loops over QuoteLike, does nothing yet)
│   ├── admin.py                 # Registers Quote, Account, Comment, QuoteLike
│   └── templates/community/     # home, login, signup, confirm, myaccount, myprofile, userprofile,
│                                #   studentsearch, coursemash, quotedetails, addarticle, addpost,
│                                #   addpics, addpicsfile, editser, editgood
│
├── biz/                         # Campus Biz marketplace
│   ├── models.py                # Service, Good, Picture, GoodPicture
│   ├── views.py                 # Listings + search, details, post service/product
│   ├── forms.py                 # PostBizForm, PostProductForm, SearchForm
│   ├── urls.py                  # /biz/ routes
│   ├── admin.py                 # Registers all four models
│   └── templates/biz/           # home, goods, details, gooddetails, post, postservice, postproduct
│
├── votes/                       # Polls
│   ├── models.py                # Poll, PollNominee, Vote
│   ├── views.py                 # home, polldetails, vote (with deadline check)
│   ├── urls.py                  # "", polldetails/<id>/, vote/<id>/
│   ├── admin.py                 # Registers Poll, PollNominee, Vote
│   └── templates/votes/         # home, polldetails
│
└── static/
    ├── static_files/            # Source static assets (STATICFILES_DIRS)
    │   ├── css/main.css         # Site stylesheet
    │   ├── js/main.js           # Show/hide helpers for profile/account tabs
    │   └── img/                 # Hero images, logo, favicon
    ├── static_root/             # collectstatic output (STATIC_ROOT), includes Django admin assets
    └── media/                   # User uploads (MEDIA_ROOT)
        ├── accounts/            # Display pictures
        ├── news/pics/           # Article pictures
        └── biz/pics/            # Service and product pictures
```

Each app also has a `migrations/` folder and an empty `tests.py`.

---

## Architecture & Patterns

| Concern | Approach |
|---|---|
| Style | Server-rendered monolith: function-based views return Django templates; no JSON API and no JavaScript framework |
| App layout | Four apps by domain: `news`, `community`, `biz`, `votes`. `biz` and `news` depend on `community.Account` / `User` |
| Template inheritance | Every page extends `news/layout.html`, which holds the header, navigation and shared responsive CSS |
| Authentication | Django's `User` model with `authenticate()` / `login()` / `logout()`. Views are protected with `@login_required(login_url='/community/login/')`. Passwords are stored with `make_password` |
| Profile extension | `community.Account` is a `OneToOneField` to `User` and holds programme, display picture, bio, editor and activation flags |
| Email verification | On sign-up, a random 6-digit number is emailed and stored in the session (`request.session['data']`); `/community/confirm/` compares the submitted value |
| Authorisation | Role checks are inline in views: `Account.editor` gates article tools; ownership checks (`provider.user == request.user`, `quoter == request.user`, `post.author == request.user`) gate edit and delete |
| Social graph | `Account.followers` / `Account.following` are `ManyToManyField`s to `User`. Follow and unfollow update both sides |
| Search | Plain `icontains` filters (`Service.service`, `Good.good`, `User.username/first_name/last_name`) |
| Forms | `ModelForm` / `Form` classes per view. The edit forms for goods and services make every field optional and only overwrite fields that were filled in |
| File uploads | `ImageField` with `upload_to` under `MEDIA_ROOT`; served by `django.conf.urls.static` when `DEBUG` is on |
| Responsive design | A 768px media query in `layout.html` swaps the desktop nav for a compact navy mobile nav and shrinks the hero banners |
| Theme | Navy and orange: navy `UZ` plus orange `C` in the logo, an orange user bar, a navy mobile nav bar |
| Client-side JS | `static/static_files/js/main.js` only toggles element visibility (e.g. showing quotes vs goods vs services on profile pages) |

---

## Data Models

| Model | File | Key Fields |
|---|---|---|
| `Account` | `community/models.py` | `user` (1:1 User), `program` (2-char code with a choices list of UZ programmes), `display_picture`, `editor`, `activated`, `bio`, `followers` / `following` (M2M User) |
| `Quote` | `community/models.py` | `quoter` (FK User), `quote` (text, max 5000), `time`; ordered newest first |
| `QuoteLike` | `community/models.py` | `liker` (FK User), `quote` (FK Quote), `time` |
| `Comment` | `community/models.py` | `quote` (FK Quote), `commenter` (FK User), `comment`, `time` |
| `DisplayPic` | `community/models.py` | `pic` (image, optional) |
| `Post` | `news/models.py` | `author` (FK User), `title`, `body`, `date_posted`, `feature_pic`, `views` |
| `PostImage` | `news/models.py` | `post` (FK Post), `image` |
| `PostComment` | `news/models.py` | `post` (FK Post), `author` (FK User), `comment` (max 400), `date_posted` |
| `Service` | `biz/models.py` | `service`, `estimate_prize`, `provider` (FK Account), `phone_or_whatsapp_number`, `description`, `feature_pic`, `date_added` |
| `Good` | `biz/models.py` | `good`, `estimate_prize`, `provider` (FK Account), `phone_or_whatsapp_number`, `description`, `feature_pic`, `date_added` |
| `Picture` | `biz/models.py` | `service` (FK Service), `picture` |
| `GoodPicture` | `biz/models.py` | `good` (FK Good), `picture` |
| `Poll` | `votes/models.py` | `title`, `end_date` |
| `PollNominee` | `votes/models.py` | `entry`, `poll` (FK Poll) |
| `Vote` | `votes/models.py` | `voter` (FK User), `poll` (FK Poll, `unique=True`), `nominee` (FK PollNominee, `unique=True`) |

---

## Views / Service Layer

There is no separate service layer; business logic lives in function-based views.

| App | Module | Transport | Purpose |
|---|---|---|---|
| `news` | `views.py` | HTML over HTTP (GET/POST) | Article feed; article detail with view counting, gallery and comment form |
| `community` | `views.py` | HTML over HTTP | Sign-up, email confirmation, login/logout, quote feed, likes, comments, follow/unfollow, student search, course mash, profiles, editor article tools, edit/delete of own content |
| `community` | `forms.py` | – | Validation, including UZ email check, unique username, password match |
| `biz` | `views.py` | HTML over HTTP | Service and goods listings with search, detail pages, posting |
| `votes` | `views.py` | HTML over HTTP | Poll list, poll detail, vote with deadline check |
| Django | `django.core.mail.send_mail` | SMTP (Gmail, port 587, TLS) | Sends the sign-up confirmation number |

---

## Navigation & Routing

Root URLconf (`uzconnect/urls.py`):

```text
/
├── admin/                          Django admin
├── ""  and  home/                  → news.urls   (both prefixes mount news)
├── community/                      → community.urls
├── biz/                            → biz.urls
└── votings/  and  votes/           → votes.urls  (both prefixes mount votes)
```

Site navigation (top bar, shown on every page): **HOME · COMMUNITY · CAMPUS BIZ · POLLS · POST · MY ACCOUNT**

```text
HOME (/)
 └── details/<id>/                          Article + comments

COMMUNITY (/community/)                     Quote feed (followed users)
 ├── details/<id>/                          Quote + comments
 ├── like/<id>/                             → back to feed
 ├── studentsearch/                         Search → follow/<id>/ · unfollow/<id>/ → userprofile/<id>/
 ├── coursemash/                            Students by programme
 ├── myaccount/                             Own quotes / goods / services
 │    ├── deletequote/<id>/  deleteser/<id>/  deletegood/<id>/
 │    ├── editser/<id>/      editgood/<id>/
 ├── myprofile/                             Profile card
 ├── add/  (editors)                        Editor landing
 │    ├── addpost/                          New article → news details
 │    └── addpics/ → addpicsfile/<id>/      Add images to own article
 ├── signup/ → confirm/ → login/ → logout/

CAMPUS BIZ (/biz/)                          Services (search)
 ├── goods/                                 Goods (search)
 ├── details/<id>/                          Service detail
 ├── gooddetails/<id>/                      Good detail
 └── post/ → postservice/ | postproduct/    Create a listing

POLLS (/votings/ or /votes/)                Poll list
 ├── polldetails/<id>/                      Nominees
 └── vote/<id>/                             Cast vote for nominee <id>
```

---

## Admin Panel

The Django admin lives at `/admin/`. Every model is registered with the default `ModelAdmin` (no customisation). The admin is also where staff set flags the UI does not expose.

| App | Registered models | Typical admin use |
|---|---|---|
| `community` | `Account`, `Quote`, `Comment`, `QuoteLike` | Set `Account.activated` and `Account.editor`; moderate quotes and comments |
| `news` | `Post`, `PostImage` | Manage articles and their images |
| `biz` | `Service`, `Good`, `Picture`, `GoodPicture` | Moderate listings; add gallery pictures (no user-facing upload view exists for these) |
| `votes` | `Poll`, `PollNominee`, `Vote` | **Create polls and nominees** (no UI for this); inspect votes |

---

## Configuration

There are no environment variables; all configuration is hard-coded in `uzconnect/settings.py`.

| Setting | Current value | What to do |
|---|---|---|
| `SECRET_KEY` | hard-coded string | **Replace before any real deployment** |
| `DEBUG` | `True` | Set to `False` in production |
| `ALLOWED_HOSTS` | `['*']` | Restrict to your domain(s) |
| `DATABASES` | SQLite at `BASE_DIR/db.sqlite3` | Swap for a production database if needed |
| `EMAIL_HOST` / `EMAIL_PORT` / `EMAIL_USE_TLS` | `smtp.gmail.com` / `587` / `True` | Match your SMTP provider |
| `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` | hard-coded Gmail address and app password | **Use your own credentials** |
| `STATIC_URL` / `STATIC_ROOT` | `/static/` / `static/static_root` | Target of `collectstatic` |
| `STATICFILES_DIRS` | `static/static_files` | Source assets |
| `MEDIA_URL` / `MEDIA_ROOT` | `/media/` / `static/media` | Where uploads are stored |
| `TIME_ZONE` | `UTC` | Change if needed |

> **Security:** the repository history contains a `SECRET_KEY` and a Gmail app password. Treat both as compromised: revoke the app password, generate a new secret key, and move them out of source control.

Recommended pattern for reading them from the environment:

```python
# uzconnect/settings.py
import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost").split(",")

EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
```

```bash
export DJANGO_SECRET_KEY="change-me"
export DJANGO_DEBUG=1
export EMAIL_HOST_USER="you@gmail.com"
export EMAIL_HOST_PASSWORD="your-gmail-app-password"
```

---

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/munacips/uzconnect.git
   cd uzconnect
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. **Install dependencies** (there is no `requirements.txt`)

   ```bash
   pip install "Django==3.0.4" Pillow pytz SQLAlchemy attrs
   ```

4. **Configure settings** – set your own `SECRET_KEY` and SMTP credentials (see [Configuration](#configuration)).

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

   A development `db.sqlite3` is committed; you can use it as-is or delete it and run the command above for a clean database.

6. **Create an admin user**

   ```bash
   python manage.py createsuperuser
   ```

   A superuser has no `Account` row yet. Log in to `/admin/` and create an `Account` for it (with `activated` ticked), otherwise the community pages, which look up `Account.objects.get(user=...)`, will fail for that user.

7. **Collect static files** (optional in development)

   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/> and log in at `/community/login/`.

9. **Activate new sign-ups** – after email confirmation, tick `activated` on the user's `Account` in `/admin/` if login still fails (see [Known Limitations](#known-limitations)). Tick `editor` to let a user publish articles.

10. **Run tests**

    ```bash
    python manage.py test
    ```

    The `tests.py` file in each app is currently an empty stub, so no tests execute.

---

## Backend Requirements (HTTP Endpoints)

Everything is served by this Django app. All routes require login unless noted. The `id` segment is a numeric primary key.

### News

| Method | Path | Purpose |
|---|---|---|
| GET | `/` or `/home/` | Article feed |
| GET, POST | `/details/<id>/` | Article detail; POST adds a comment |

### Community

| Method | Path | Purpose |
|---|---|---|
| GET, POST | `/community/` | Feed of followed users' quotes; POST creates a quote |
| GET, POST | `/community/signup/` | Register (no login required) |
| GET, POST | `/community/confirm/` | Enter the emailed confirmation number (no login required) |
| GET, POST | `/community/login/` | Log in (no login required) |
| GET | `/community/logout/` | Log out |
| GET, POST | `/community/coursemash/` | List students by programme |
| GET, POST | `/community/studentsearch/` | Search students |
| GET | `/community/follow/<id>/` | Follow a user |
| GET | `/community/unfollow/<id>/` | Unfollow a user |
| GET | `/community/myaccount/` | Own quotes, goods, services |
| GET | `/community/myprofile/` | Own profile |
| GET | `/community/userprofile/<id>/` | Another user's profile |
| GET, POST | `/community/details/<id>/` | Quote detail; POST adds a comment |
| GET | `/community/like/<id>/` | Like a quote |
| GET | `/community/deletequote/<id>/` | Delete own quote |
| GET | `/community/deleteser/<id>/` | Delete own service |
| GET | `/community/deletegood/<id>/` | Delete own good |
| GET, POST | `/community/editser/<id>/` | Edit own service |
| GET, POST | `/community/editgood/<id>/` | Edit own good |
| GET | `/community/add/` | Editor landing (editors only) |
| GET, POST | `/community/addpost/` | Publish an article (editors only) |
| GET | `/community/addpics/` | List own articles (editors only) |
| GET, POST | `/community/addpicsfile/<id>/` | Upload extra images to own article |

### Campus Biz

| Method | Path | Purpose |
|---|---|---|
| GET, POST | `/biz/` | Services list; POST searches |
| GET, POST | `/biz/goods/` | Goods list; POST searches |
| GET | `/biz/details/<id>/` | Service detail |
| GET | `/biz/gooddetails/<id>/` | Good detail |
| GET | `/biz/post/` | Choose service or product |
| GET, POST | `/biz/postservice/` | Create a service listing |
| GET, POST | `/biz/postproduct/` | Create a product listing |

### Polls

| Method | Path | Purpose |
|---|---|---|
| GET | `/votings/` or `/votes/` | Poll list |
| GET | `/votings/polldetails/<id>/` | Poll nominees |
| GET | `/votings/vote/<id>/` | Vote for nominee `<id>` |

### Other

| Method | Path | Purpose |
|---|---|---|
| GET | `/admin/` | Django admin |
| GET | `/static/…`, `/media/…` | Static files and uploads (served by Django only while `DEBUG = True`) |

---

## Deployment

The repository contains **no Dockerfile, docker-compose file or CI configuration**. The notes below follow from `settings.py`.

Checklist before going live:

```bash
# 1. Production settings: DEBUG=False, a new SECRET_KEY, a real ALLOWED_HOSTS,
#    your own SMTP credentials (see Configuration).

# 2. Gather static assets into STATIC_ROOT (static/static_root)
python manage.py collectstatic --noinput

# 3. Apply migrations
python manage.py migrate

# 4. Serve through a WSGI server (entry point: uzconnect.wsgi.application)
pip install gunicorn
gunicorn uzconnect.wsgi:application --bind 0.0.0.0:8000
```

Hosting notes:

- With `DEBUG = False`, Django does **not** serve `/static/` or `/media/`. Have a web server (e.g. nginx) serve `static/static_root` at `/static/` and `static/media` at `/media/`.
- User uploads are written to `static/media/`, so persist that directory (volume or object storage) across deployments.
- The database is a single SQLite file, so persist `db.sqlite3` too, or move to a server database for multi-process hosting.
- An ASGI entry point (`uzconnect.asgi`) also exists, but nothing in the app is async.

---

## Known Limitations

Observed in the current code:

| Area | Behaviour |
|---|---|
| Email confirmation | `community.views.confirm` sets `acc.activated = True` but never calls `acc.save()`, so activation does not persist; activate accounts in `/admin/` |
| Login redirect | `log_in` redirects to `request.GET.get('next')`, which is `None` when the login URL is opened without `?next=` |
| Voting | `Vote.poll` and `Vote.nominee` are both `unique=True`, which allows only one vote per poll across all users (and one per nominee) rather than one per voter |
| Poll management | There is no UI to create polls or nominees; use `/admin/` |
| Imports | `biz/models.py` imports `sqlalchemy`, `biz/forms.py` imports `attr`, so both packages must be installed even though they are unused |
| Programme codes | Some two-letter codes in `Account.PROGRAM` repeat for different programmes (e.g. `aj`, `ca`, `cb`, `cc`, `f`) |
| State-changing GET | Like, follow, unfollow and delete actions are plain GET links |
| Tests | All `tests.py` files are empty |
| Secrets | `SECRET_KEY` and the Gmail password are committed in `settings.py` |
