# faaji-brew-afromart Introduction

An e-commerce app created for the purpose of meeting the assessment criteria of my final portfolio project 5 as a full-stack software developer at Code Institute, Dublin, Ireland. I built this fully functioning e-commerce website.

**Portfolio Project 5 - A final E-Commerce Project for a Level 5 Diploma in Full-Stack Software Development**
**Code Institute, Dublin**

---

<div align="center">

# 🛍️ Faaji & Brew AfroMart

### An authentic West African lifestyle e-commerce platform

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-Payments-635BFF?style=for-the-badge&logo=stripe&logoColor=white)
![Heroku](https://img.shields.io/badge/Deployed-Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-116%20Passing-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white)
![PEP8](https://img.shields.io/badge/PEP8-Compliant-blue?style=for-the-badge&logo=python&logoColor=white)

**[🌐 View the Live Site](https://faaji-brew-afromart-0cba904df962.herokuapp.com/)** &nbsp;•&nbsp; **[💻 View the Repository](https://github.com/Emmy-Dare274/faaji-brew-afromart)**

</div>

---

Faaji & Brew AfroMart is a full-stack e-commerce web application built with Django, selling authentic West African fabrics, spices, beads, jewellery, and homeware. It was born as a natural extension of Faaji & Brew Palace, a real restaurant whose guests kept asking where they could buy the fabrics on the walls and the spices used in the kitchen. This platform is that answer: a complete, secure, real-money-capable online store, built from scratch as a personal portfolio project for a Level 5 Diploma in Full-Stack Software Development.

Every feature described in this document is genuinely working on the live deployment, not a mockup. You can browse the catalogue, create a real account, add products to a basket, and complete an actual purchase using Stripe's test card system, right now, without needing to download or install anything.

<a name="table-of-contents"></a>
## 📑 Table of Contents

1. [UX Design](#ux-design)
   - [Strategy](#strategy)
   - [Scope](#scope)
   - [Structure](#structure)
   - [Skeleton — Wireframes](#skeleton--wireframes)
   - [Surface — Design System](#surface--design-system)
2. [Agile Methodology & User Stories](#agile-methodology--user-stories)
3. [Features](#features)
   - [Navigation & Browsing](#navigation--browsing)
   - [Product Discovery](#product-discovery)
   - [Reviews](#reviews)
   - [Basket & Checkout](#basket--checkout)
   - [User Accounts](#user-accounts)
   - [Staff Tools](#staff-tools)
   - [Marketing & SEO](#marketing--seo)
   - [Future Features](#future-features)
4. [Database Schema](#database-schema)
5. [Marketing](#marketing)
6. [Technologies Used](#technologies-used)
7. [Testing](#testing)
8. [Bugs Found and Fixed](#bugs-found-and-fixed)
9. [Deployment](#deployment)
   - [Local Development](#local-development)
   - [Heroku Deployment](#heroku-deployment)
10. [Credits](#credits)

---

<a name="ux-design"></a>
## 🎨 UX Design

This project was planned using the five-plane UX design model: Strategy, Scope, Structure, Skeleton, and Surface. Each plane's decisions fed directly into the next, from the earliest question of who the site is for, through to the exact shade of teal used on a button.

<a name="strategy"></a>
### Strategy

**Site goals:**
- Give West African diaspora customers, and anyone curious about the culture, a genuine, trustworthy place to buy real ingredients, fabrics, and handmade goods online
- Convert the goodwill already built by the Faaji & Brew Palace restaurant into a second, complementary revenue stream
- Build a store that feels warm and personal rather than like a generic template, reflecting the actual culture behind the products

**User goals:**
- Find a specific product quickly, whether browsing by category or searching directly
- Trust that a review is genuine, written by someone who actually bought the item
- Check out quickly and securely, with clear delivery costs shown upfront
- Track past orders and reorder favourites without re-entering everything from scratch
- Feel confident giving a business their card details, especially one they may not have heard of before

<a name="scope"></a>
### Scope

The scope was deliberately kept to what a real small business actually needs to start selling online, rather than every feature a large marketplace might eventually want:

**In scope:** product catalogue with categories and variants, search and filtering, a persistent basket that survives login, secure card payment, verified purchase reviews, user accounts with saved addresses and order history, a staff-only management area for products and categories that doesn't require the Django admin, and a full SEO and accessibility pass.

**Out of scope for this version:** multi-currency support, third-party marketplace integrations (eBay, Amazon), a native mobile app, and multi-vendor seller accounts. These are noted honestly in [Future Features](#future-features) rather than left unmentioned.

<a name="structure"></a>
### Structure

The site is organised around six independent Django apps, each owning one area of responsibility:

| App | Responsibility |
|---|---|
| `core` | Static pages - home, our story, FAQ, contact, legal pages, the 404 page, SEO infrastructure |
| `products` | The catalogue - categories, products, variants, images, reviews, and all staff management tools |
| `basket` | The shopping basket, for both guests and logged-in users |
| `checkout` | Address collection, Stripe payment, order creation, and the webhook that confirms payment server-side |
| `profiles` | User accounts, saved delivery details, order history, reordering, and wishlists |
| `marketing` | Newsletter signup and confirmation |

This separation means each app can be reasoned about, and tested, largely on its own - a change to how reviews work never risks breaking checkout, because they don't share code beyond the shared `Product` model itself.

<a name="skeleton--wireframes"></a>
### Skeleton — Wireframes

Wireframes were created before any code was written, to settle on page layout and user flow ahead of time. The final build followed these closely, though a handful of pages (My Account, staff tools) grew additional functionality once the underlying data model was in place.

<details>
<summary><strong>Click to view all 12 wireframes</strong></summary>

#### Home Page
![Homepage Wireframe](docs/wireframes/01_homepage.jpeg)

#### Category Page
![Category Page Wireframe](docs/wireframes/02_category.jpeg)

#### Products Page
![Products Page Wireframe](docs/wireframes/03_products.jpeg)

#### Product Detail Page
![Product Detail Wireframe](docs/wireframes/04_product_detail.jpeg)

#### Our Story Page
![Our Story Wireframe](docs/wireframes/05_our_story.jpeg)

#### Basket Page
![Basket Wireframe](docs/wireframes/06_basket.jpeg)

#### Checkout Page
![Checkout Wireframe](docs/wireframes/07_checkout.jpeg)

#### My Account Page
![My Account Wireframe](docs/wireframes/08_my_account.jpeg)

#### Favourites Page
![Favourites Wireframe](docs/wireframes/09_favorites.jpeg)

#### Login Page
![Login Wireframe](docs/wireframes/10_login.jpeg)

#### Register Page
![Register Wireframe](docs/wireframes/11_register.jpeg)

#### 404 Page
![404 Page Wireframe](docs/wireframes/12_404_page.jpeg)

</details>

<a name="surface--design-system"></a>
### Surface — Design System

**Colour palette**

| Swatch | Name | Hex | Used for |
|---|---|---|---|
| 🟦 | Indigo Deep | `#131B3F` | Primary dark backgrounds, navbar, footer |
| 🟦 | Indigo Mid | `#202A5E` | Gradient accents alongside Indigo Deep |
| 🟩 | Teal | `#2A9D8F` | Primary call-to-action colour, links, brand accent |
| 🟩 | Teal Light | `#3FC1B0` | Gradient partner to Teal, hover states |
| ⬜ | Cream | `#FAFAF8` | Main page background |
| ⬛ | Ink | `#1A1A1A` | Body text |

**Typography**

- **Headings** use *Cormorant Garamond*, a serif typeface chosen to give the brand an editorial, boutique feel rather than a generic tech-startup look.
- **Body text** uses *Inter*, a clean, highly legible sans-serif, keeping product descriptions and long-form text easy to read at any size.

**Imagery**

Product photography and lifestyle imagery were chosen to reflect genuine West African fabrics, spices, and craftsmanship, reinforcing the story behind the brand rather than using generic stock photography that could belong to any store.

---

<a name="agile-methodology--user-stories"></a>
## 📋 Agile Methodology & User Stories

The whole project was planned and tracked using a GitHub Projects Kanban board, with every piece of work written as a real user story before it was built, not decided ad hoc while coding.

**Board workflow:** every story moved through four columns — **ToDo** → **In Progress** → **In-Review** → **Done** — with nothing skipped, so work was always visibly either not started, actively being built, ready for a final check, or genuinely finished.

**Prioritisation:** stories were labelled using MoSCoW prioritisation (**Must-have**, **Should-have**, **Could-have**), so that if time ever ran short, it was always clear which stories were non-negotiable for a working e-commerce platform (accounts, basket, checkout, payment) versus which were valuable but secondary (a 404 page, homepage testimonials).

**Story format:** every story was written from the user's point of view, with explicit acceptance criteria, in the shape:

> **As a** [type of user], **I want** [a goal], **so that** [a reason].
> **Acceptance Criteria:** a specific, checkable list of what "done" means.

This mattered in practice, not just on paper — several stories (particularly around SEO and testing) were written specifically to close gaps identified after earlier work, with acceptance criteria precise enough that "done" was never a matter of opinion.

### Key user stories delivered

| # | User Story | Status |
|---|---|---|
| Login/logout | As a customer, I want to log in and log out securely | ✅ Done |
| Auth status at a glance | As a customer, I want to see whether I'm logged in without hunting for it | ✅ Done |
| Restricted pages | As a site owner, I want private pages blocked from anyone not logged in | ✅ Done |
| Saved delivery addresses | As a returning customer, I want my delivery details remembered | ✅ Done |
| Browse by category | As a shopper, I want to browse products by category | ✅ Done |
| Filter by price | As a shopper, I want to filter products by price range | ✅ Done |
| Basket management | As a shopper, I want to add, update, and remove basket items with the total updating live | ✅ Done |
| Order confirmation | As a customer, I want confirmation that my order and payment succeeded | ✅ Done |
| Order history | As a customer, I want to view my past orders and their status | ✅ Done |
| Shop from wishlist | As a customer, I want to save products and buy them later | ✅ Done |
| Write a review | As a customer, I want to review a product I've genuinely bought | ✅ Done |
| Edit/delete a review | As a customer, I want control over a review I've written | ✅ Done |
| Moderate reviews | As a site owner, I want to approve or reject reviews before they go public | ✅ Done |
| Staff product management | As a site owner, I want to manage products without needing the Django admin | ✅ Done |
| Find any page from a link | As a search engine or user, I want every page reachable and indexed | ✅ Done |
| Helpful 404 page | As a visitor, I want a broken link to still help me find what I need | ✅ Done |
| Accurate page descriptions | As a search engine user, I want search results that reflect the real page content | ✅ Done |
| Thoroughly tested | As the site owner, I want automated tests and a documented manual test pass | ✅ Done |
| Real testimonials | As a shopper, I want to see genuine reviews from other customers on the homepage | ✅ Done |
| Full documentation | As anyone assessing this project, I want a README that actually explains it | ✅ Done |

---

<a name="features"></a>
## ✨ Features

<a name="navigation--browsing"></a>
### Navigation & Browsing

- A responsive navbar with direct links to every top-level category, plus a **Special Offers** dropdown filtered by category
- Global product search, reachable from both the navbar and the homepage
- A footer present on every page, with quick links to every static page, every category, the social media presence, and a working newsletter signup
- A homepage category rail that scrolls smoothly on touch devices, with scroll-snap so cards settle neatly into place, and a subtle edge fade hinting there's more to see

![Homepage](docs/screenshots/home.jpg)
![Homepage on mobile](docs/screenshots/home-mobile.jpg)
![Footer](docs/screenshots/footer.png)

<a name="product-discovery"></a>
### Product Discovery

- A full category overview page for browsing the whole catalogue at a glance
- Product listing pages with live search, minimum/maximum price filtering, and sorting by price, rating, or name in either direction
- A detailed product page with a full photo carousel, thumbnail navigation, live stock status, and support for product variants (size, colour) where applicable
- A **Special Offers** page surfacing discounted products, filterable by category

![Category overview](docs/screenshots/category-overview.jpg)
![Product listing with filters](docs/screenshots/product-list.jpg)
![Product detail page](docs/screenshots/product-detail.jpg)

<a name="reviews"></a>
### Reviews

- Only a customer who has genuinely bought a product can review it — reviews can't be faked by someone who never purchased
- One review per customer per product, editable or deletable at any time by whoever wrote it
- Every new or edited review starts as pending and only becomes publicly visible once a staff member approves it from a dedicated moderation queue
- Approved, featured reviews are pulled onto the homepage automatically as customer testimonials

![Product reviews](docs/screenshots/product-reviews.png)
![Staff review moderation queue](docs/screenshots/review-moderation.jpg)

<a name="basket--checkout"></a>
### Basket & Checkout

- A basket that works for guests via their session, and automatically merges into their account the moment they log in, so nothing added before logging in is lost
- Live quantity updates, line totals, and a running basket total, with a clear progress indicator toward free delivery
- Secure checkout handled entirely by Stripe, supporting standard cards, 3D Secure authentication, and correctly handling declined payments without creating a broken order
- A genuine order confirmation page and email, generated only once Stripe has actually confirmed payment server-side via a webhook, not merely because the customer's browser reached a "success" URL

![Basket](docs/screenshots/basket.jpg)
![Checkout](docs/screenshots/checkout.jpg)
![Order confirmation](docs/screenshots/checkout-success.jpg)

<a name="user-accounts"></a>
### User Accounts

- Full account registration with mandatory email verification before login is allowed, and a secure password reset flow — every one of these pages is custom-styled to match the brand, not left as django-allauth's bare default templates
- A My Account page for managing saved delivery details, so returning customers never have to retype their address
- A complete order history, with a one-click **Reorder** button that adds every available item from a past order back into the basket, automatically skipping anything since discontinued or sold out rather than failing the whole action
- A personal wishlist, addable and removable from any product card, with logged-out visitors prompted to log in rather than the action failing silently
- A customer service contact us page, users and visitors can visit through the footer and make enquiries or complaint.

![Login](docs/screenshots/login.jpg)
![Sign up](docs/screenshots/signup.jpg)
![Contact Us](docs/screenshots/contact-us.jpg)
![My Account](docs/screenshots/my-account.jpg)
![Order history](docs/screenshots/order-history.jpg)
![Wishlist](docs/screenshots/wishlist.jpg)

<a name="staff-tools"></a>
### Staff Tools

- A dedicated staff dashboard, reachable only by staff accounts, linking to every management tool in one place
- Full product management — add, edit, and deactivate products, including managing multiple photos and variants together on a single page — entirely from the live site, with no need to touch the Django admin
- Full category management, including add, edit, and delete
- A genuine safety rule, not just a convenience: a product or category that has ever appeared in a real customer order **cannot** be permanently deleted, only deactivated, so order history can never be silently destroyed by an accidental click

![Staff dashboard](docs/screenshots/staff-dashboard.jpg)
![Staff product list](docs/screenshots/staff-product-list.jpg)
![Staff product add/edit form](docs/screenshots/staff-product-form.jpg)

<a name="marketing--seo"></a>
### Marketing & SEO

- A dynamically generated `sitemap.xml` listing every product, category, and static page, and a `robots.txt` that always references the correct live host
- A genuinely unique, accurate title and meta description on every single page of the site, including every step of the login and password reset flow, with zero duplicated or placeholder text anywhere
- A custom, branded 404 page with a working search box and clear navigation, rather than Django's bare default error page
- A custom favicon matching the site's own brand mark, visible in the browser tab and as a home-screen icon on mobile
- A cookie consent banner, remembered across visits once dismissed
- A real newsletter signup with double confirmation: a genuine email is sent, and the subscription only activates once the link inside it is clicked

![Custom 404 page](docs/screenshots/404-page.jpg)

<a name="future-features"></a>
### Future Features

Documented honestly as deliberate scope decisions, not oversights:

- **Guest checkout** — checkout currently requires an account, a deliberate choice for this version to keep order history and reordering reliable, but a true guest checkout path is a natural next step
- **Multi-currency support** — currently priced in USD only
- **Product recommendations** — a "customers also bought" section on the product detail page
- **Wishlist sharing** — letting a customer share their wishlist with someone else, useful for gift-giving
- **A richer staff analytics dashboard** — sales trends and stock alerts, beyond the current product/category management tools

---
<a name="database-schema"></a>
## 🗄️ Database Schema

The database uses PostgreSQL in production (hosted on Neon) and falls back to SQLite for local development when no `DATABASE_URL` is set, keeping local testing completely separate from real customer data.

```mermaid
erDiagram
    CATEGORY ||--o{ PRODUCT : contains
    PRODUCT ||--o{ PRODUCTIMAGE : has
    PRODUCT ||--o{ PRODUCTVARIANT : has
    PRODUCT ||--o{ REVIEW : has
    PRODUCT ||--o{ BASKETITEM : "added to"
    PRODUCT ||--o{ ORDERLINEITEM : "sold as"
    PRODUCT ||--o{ WISHLISTITEM : "saved as"
    PRODUCTVARIANT ||--o{ BASKETITEM : "chosen in"
    PRODUCTVARIANT ||--o{ ORDERLINEITEM : "chosen in"

    USER ||--o| USERPROFILE : has
    USER ||--o{ BASKET : owns
    USER ||--o| WISHLIST : owns
    USER ||--o{ ORDER : places
    USER ||--o{ REVIEW : writes

    BASKET ||--o{ BASKETITEM : contains
    ORDER ||--o{ ORDERLINEITEM : contains
    WISHLIST ||--o{ WISHLISTITEM : contains

    CATEGORY {
        string name
        string slug
        text description
        image image
        bool is_active
        bool show_in_main_nav
    }
    PRODUCT {
        string name
        string slug
        string sku
        text description
        decimal price
        int stock_quantity
        bool is_featured
        bool is_active
    }
    PRODUCTIMAGE {
        image image
        string alt_text
        bool is_primary
    }
    PRODUCTVARIANT {
        string variant_type
        string value
        int stock_quantity
        decimal price_adjustment
    }
    REVIEW {
        int rating
        string title
        text body
        bool is_approved
        bool is_featured
    }
    USER {
        string username
        string email
        string password
    }
    USERPROFILE {
        string default_full_name
        string default_phone_number
        string default_address_line1
        string default_town_or_city
        string default_postcode
        string default_country
    }
    BASKET {
        string session_key
    }
    BASKETITEM {
        int quantity
    }
    ORDER {
        string order_number
        string full_name
        string email
        string status
        decimal order_total
        decimal delivery_cost
        decimal grand_total
    }
    ORDERLINEITEM {
        int quantity
        decimal price_at_purchase
    }
    WISHLIST {
        datetime created_at
    }
    WISHLISTITEM {
        datetime added_at
    }
```

**A note on reading the diagram:** `||` means "exactly one," `o{` means "zero or many," and `o|` means "zero or one." So `USER ||--o{ BASKET : owns` reads as "one User owns zero or many Baskets" — reflecting that `Basket.user` is a plain foreign key, not a strict one-to-one link, and that guest baskets exist with no user attached at all.

**Relationship types**

| Relationship | Type | Meaning |
|---|---|---|
| Category → Product | One-to-Many | One category holds many products; each product belongs to exactly one category |
| Product → ProductImage | One-to-Many | One product can have many photos |
| Product → ProductVariant | One-to-Many | One product can have many variants (sizes, colours) |
| Product → Review | One-to-Many | One product can receive many reviews |
| User → Review | One-to-Many | One user can write many reviews (one per product, enforced separately) |
| User → UserProfile | **One-to-One** | Each user has exactly one profile, and each profile belongs to exactly one user |
| User → WishList | **One-to-One** | Each user has exactly one wishlist |
| User → Basket | One-to-Many | A user can have more than one basket row over time; application logic keeps only one active at a time |
| User → Order | One-to-Many | One user can place many orders over time |
| Basket → BasketItem | One-to-Many | One basket holds many line items |
| Order → OrderLineItem | One-to-Many | One order holds many line items |
| WishList → WishListItem | One-to-Many | One wishlist holds many saved products |
| Product → BasketItem / OrderLineItem / WishListItem | One-to-Many | One product can appear in many baskets, orders, and wishlists across different users |

Every relationship in this schema is either one-to-one or one-to-many — there are no many-to-many fields anywhere in the data model. Where something might look like a many-to-many relationship at first glance, such as products appearing in many baskets while baskets hold many products, it's actually implemented as two separate one-to-many relationships meeting at a middle table (`BasketItem`, `OrderLineItem`, `WishListItem`), which is what lets each of those middle tables carry its own extra data — a basket item's quantity, an order line's locked-in purchase price, and so on — something a true many-to-many field couldn't do on its own.

| Model | Key Fields | Relationships |
|---|---|---|
| **Category** | name, slug, description, image, is_active, show_in_main_nav | Has many Products |
| **Product** | category, name, slug, sku, description, price, stock_quantity, is_featured, is_active | Belongs to Category · Has many ProductImages, ProductVariants, Reviews |
| **ProductImage** | product, image, alt_text, is_primary | Belongs to Product |
| **ProductVariant** | product, variant_type, value, stock_quantity, price_adjustment | Belongs to Product |
| **Review** | product, user, rating, title, body, is_approved, is_featured | Belongs to Product and User · one review per user per product |
| **Basket** | user (nullable), session_key | Has many BasketItems |
| **BasketItem** | basket, product, variant (nullable), quantity | Belongs to Basket and Product |
| **Order** | user, order_number, full_name, address fields, status, order_total, delivery_cost, grand_total | Belongs to User · Has many OrderLineItems |
| **OrderLineItem** | order, product, variant (nullable), quantity, price_at_purchase | Belongs to Order and Product |
| **UserProfile** | user, default full name/phone/address fields | One-to-one with User |
| **WishList** | user | One-to-one with User · Has many WishListItems |
| **WishListItem** | wishlist, product | Belongs to WishList and Product · one entry per product per wishlist |
| **NewsletterSubscriber** | email, confirmed, confirmation_token | Standalone |

A deliberate design decision worth calling out: `OrderLineItem.price_at_purchase` stores a frozen copy of the price at the moment of sale, independent of `Product.price`. If a product's price changes later, every past order correctly keeps showing what the customer actually paid, not today's price.

---


<a name="marketing"></a>
## 📣 Marketing

### Facebook Business Page

A real Facebook Business Page was created for Faaji & Brew AfroMart as part of the site's marketing strategy, linking back to the live store from the page's intro, about section, and posts.

[View the Facebook Business Page](https://www.facebook.com/share/17QgB9TWdd/)

![Facebook Business Page](docs/marketing/facebook-business-page.jpg)

The page is linked from the site's footer, under both the social icons and the Company column, opening in a new tab.

### Other Social Platforms

Instagram, TikTok, X, and YouTube icons are also present in the footer. Since dedicated business accounts haven't been created on those platforms yet, each currently links to that platform's own homepage rather than a dead or placeholder link, so every icon in the footer does something genuinely useful. These will be updated to point to real business accounts as they're created.

### Newsletter

A working email newsletter signup sits on the homepage. A new subscriber receives a genuine confirmation email and is only added as an active subscriber once they click the link inside it, avoiding fake or mistyped signups.

---

<a name="technologies-used"></a>
## 🛠️ Technologies Used

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

**Backend**

- **[Django](https://www.djangoproject.com/)** — the core web framework
- **[django-allauth](https://docs.allauth.org/)** — registration, login, email verification, password reset
- **[django-countries](https://pypi.org/project/django-countries/)** — country selection at checkout
- **PostgreSQL** (via **[Neon](https://neon.tech/)**) — production database
- **[Stripe](https://stripe.com/)** — payment processing and webhooks
- **[Cloudinary](https://cloudinary.com/)** via `django-cloudinary-storage` — image hosting and delivery
- **[Gunicorn](https://gunicorn.org/)** — the production web server
- **[WhiteNoise](https://whitenoise.readthedocs.io/)** — static file serving

**Frontend**

- **Bootstrap 5** — layout, grid, and component styling
- **Bootstrap Icons** — every icon across the site
- **Vanilla JavaScript** — basket updates, wishlist toggling, cookie consent, toast notifications, no framework or build step

**Tools & Platforms**

![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=flat-square&logo=heroku&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white)

- **GitHub Projects** — Kanban board and issue tracking
- **GitHub Codespaces** — primary development environment
- **W3C Markup Validation Service** and **W3C CSS Validation Service** — HTML/CSS validation
- **JSHint** — JavaScript linting
- **flake8** — Python PEP8 compliance
- **Google Lighthouse** — performance, accessibility, best practice, and SEO auditing

---

<a name="testing"></a>
## 🧪 Testing

Testing is documented in full detail in **[TESTING.md](TESTING.md)**, including a complete traceability table mapping every automated test back to the specific user story it verifies. Summary:

- **116 automated tests** across all six apps, covering models, forms, and views, run with Django's own test runner (`python manage.py test`) — currently passing in full
- **PEP8 compliant** — a clean `flake8` run across the entire codebase, with zero warnings
- **HTML validated** — every unique page template checked against the W3C Markup Validation Service
- **CSS validated** — the full stylesheet checked against the W3C CSS Validation Service
- **JavaScript linted** — all four custom JS files checked with JSHint
- **Lighthouse audited** — Performance, Accessibility, Best Practices, and SEO scored on mobile and desktop across five key pages
- **A full manual test pass** — real click-through testing of every feature in a real browser, including genuine Stripe test-card purchases (standard, 3D Secure, and declined cards), documented with real results

See [TESTING.md](TESTING.md) for the complete breakdown, every test case, and every validator screenshot.

---

<a name="bugs-found-and-fixed"></a>
## 🐛 Bugs Found and Fixed

Real problems, found and fixed during development, rather than a suspiciously bug-free story:

| Bug | Cause | Fix |
|---|---|---|
| Heroku build failing | `.python-version` was pinned to a Python release Heroku's buildpack didn't yet support | Pinned to Python 3.12 |
| `collectstatic` crashing on deploy | A third-party package's bundled CSS referenced an image file that didn't exist, and Django's strict static storage treated that as fatal | Added a custom static storage class that fails gracefully instead of crashing the whole build |
| Order confirmation emails never sending | `DEFAULT_FROM_EMAIL` was missing its closing `>` bracket, an invalid email header the SMTP library correctly rejected | Corrected the config value |
| A customer's own approved review invisible to themselves | A queryset filter meant to prevent something else accidentally excluded the logged-in user's own review from the public list | Removed the incorrect filter |
| Setting basket quantity to exactly 0 didn't remove the item | A quantity-sanitising function treated 0 as invalid input and silently reset it to 1, even though the update view specifically used 0 as the signal to remove an item | Added an explicit "zero is allowed here" flag for the one place it's meant to be valid |
| Product listing pages loading slowly (3+ seconds) | Every product's image lookup ran extra, unbatched database queries — a classic N+1 query problem, invisible on SQLite but very visible against a real remote Postgres database | Rewrote the image lookup to work with Django's `prefetch_related`, cutting dozens of queries per page down to one |
| Invalid HTML on every page showing a star rating | A `<p>` tag included a separate template that itself opened its own `<p>`, illegally nesting one paragraph inside another | Restructured the markup so no paragraph is ever nested inside another |
| Skipped heading levels flagged by the HTML validator | The footer's column headings jumped straight from `<h2>` to `<h6>`, skipping three heading levels that screen readers rely on for navigation | Added a hidden anchor heading and corrected the footer headings to `<h3>`, with a CSS override so the visual design didn't change |
| Anonymous wishlist clicks failing with no feedback | The wishlist toggle endpoint had no handling at all for a logged-out visitor | Added an explicit check that returns a proper prompt to log in |
| Staff could add a product's photos, but rows silently vanished past a certain count | Two separate inline forms on the same page defaulted to an identical internal form-field prefix, so the browser confused one form's fields with the other's | Gave each form its own explicit, distinct prefix |
| The site occasionally showed Chrome's "Dangerous site" warning | Heroku's shared `*.herokuapp.com` domain occasionally inherits a reputation flag from unrelated apps hosted on the same domain space — confirmed via server logs showing the flagged requests never even reached the application | Reported as a false positive to Google Safe Browsing; not a defect in the application itself |

---

<a name="deployment"></a>
## 🚀 Deployment

<a name="local-development"></a>
### Local Development

**Prerequisites:** Python 3.12, Git, and a code editor.

```bash
git clone https://github.com/Emmy-Dare274/faaji-brew-afromart.git
cd faaji-brew-afromart
python -m venv .venv
source .venv/Scripts/activate    # Windows Git Bash
# or: .venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

Create an `env.py` file in the project root (this file is git-ignored and never committed) containing:

```python
import os

os.environ.setdefault("SECRET_KEY", "your-django-secret-key")
os.environ.setdefault("DEBUG", "True")

os.environ.setdefault("CLOUDINARY_CLOUD_NAME", "your-cloudinary-cloud-name")
os.environ.setdefault("CLOUDINARY_API_KEY", "your-cloudinary-api-key")
os.environ.setdefault("CLOUDINARY_API_SECRET", "your-cloudinary-api-secret")

os.environ.setdefault("STRIPE_PUBLIC_KEY", "your-stripe-publishable-key")
os.environ.setdefault("STRIPE_SECRET_KEY", "your-stripe-secret-key")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "your-stripe-webhook-signing-secret")

os.environ.setdefault("EMAIL_HOST_USER", "your-gmail-address")
os.environ.setdefault("EMAIL_HOST_PASS", "your-gmail-app-password")
os.environ.setdefault("DEFAULT_FROM_EMAIL", "AfroMart <your-gmail-address>")
```

`DATABASE_URL` is deliberately left unset for local development, so the project automatically falls back to a local SQLite database, keeping local testing completely separate from the live Neon Postgres database.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_products
python manage.py runserver
```

To test Stripe payments locally, run the Stripe CLI in a second terminal so webhook events reach your machine:

```bash
stripe login
stripe listen --forward-to localhost:8000/checkout/wh/
```

<a name="heroku-deployment"></a>
### Heroku Deployment

1. Create a new Heroku app
2. Under **Settings → Config Vars**, add every variable listed in the `env.py` example above, plus `DATABASE_URL` pointing to a real Neon Postgres connection string, and set `DEBUG` to `False`
3. Connect the app to this GitHub repository, or add the Heroku git remote manually:
```bash
   heroku git:remote -a your-app-name
```
4. Push to deploy:
```bash
   git push heroku main
```
5. Heroku automatically runs `python manage.py migrate` on every release (defined in the `Procfile`), and `collectstatic` runs automatically during the build
6. In the Stripe Dashboard, add a live webhook endpoint pointing to `https://your-app-name.herokuapp.com/checkout/wh/`, and copy its signing secret into the `STRIPE_WEBHOOK_SECRET` config var

The live version of this project is deployed exactly this way, at [faaji-brew-afromart-0cba904df962.herokuapp.com](https://faaji-brew-afromart-0cba904df962.herokuapp.com/).

---

<a name="credits"></a>
## 🙏 Credits

**Content:** All product descriptions, page copy, and the brand story were written specifically for this project.

**Code:** Every line of application code was written specifically for this project. Django, Bootstrap, Stripe, Cloudinary, and django-allauth were used strictly according to their own official documentation.

**A personal note:** this project grew far beyond its original scope, from a simple product catalogue into a full storefront with staff tooling, verified reviews, and a genuine automated test suite. Every bug listed above was a real one, found by actually testing the site rather than assuming it worked, and every fix was verified before moving on. That process, more than any single feature, is what this project is really about.

### Code and Learning Resources

- **[John Elder — Codemy.com](https://codemy.com/)** — John's Django and Python courses provided invaluable guidance for me throughout this project. His teaching style made Django's MVT pattern, authentication flows, and database design approachable and practical. The depth of his Full-Stack Django course content shaped how this project was structured and built.

- **[Code Institute](https://codeinstitute.net/)** — The LMS course material, walkthrough projects (especially Boutique Ado walkthrough), and the structured curriculum for Portfolio Project 5 provided me with the foundation for this build.


### Media

All photography used on the Faaji & Brew AfroMart website was sourced from **[pinterest](https://www.pinterest.com/) and [pixabay](https://pixabay.com/)**, a platform offering high-quality, freely usable images under the [Unsplash License](https://unsplash.com/license).


### Acknowledgements

This project was completed as part of my **Level British 5 Diploma in Full-Stack Software Development** at **Code Institute, Dublin**. The support of the Code Institute tutors, mentors, account department, and student community throughout this diploma has been outstanding.

* I thank God Almighty for giving me the strength to stay awake all night to code and debug, even though it was so difficult for me, but all praises to God for supporting and giving me the right frame of mind to learn, collaborate with others in different learning communities and platforms to ensure the completion of this portfolio project five (5). 

---

*Faaji & Brew AfroMart — An authentic West African lifestyle e-commerce platform*

*by: Emmanuel Oluwatosin Oluwadare — Code Institute final Portfolio Project 5 — 2026*

<div align="center">

**[⬆ Back to Top](#-faaji--brew-afromart)**

</div>
