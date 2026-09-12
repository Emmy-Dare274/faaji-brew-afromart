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

![Homepage](docs/screenshots/home.png)
![Homepage on mobile](docs/screenshots/home-mobile.png)
![Footer](docs/screenshots/footer.png)

<a name="product-discovery"></a>
### Product Discovery

- A full category overview page for browsing the whole catalogue at a glance
- Product listing pages with live search, minimum/maximum price filtering, and sorting by price, rating, or name in either direction
- A detailed product page with a full photo carousel, thumbnail navigation, live stock status, and support for product variants (size, colour) where applicable
- A **Special Offers** page surfacing discounted products, filterable by category

![Category overview](docs/screenshots/category-overview.png)
![Product listing with filters](docs/screenshots/product-list.png)
![Product detail page](docs/screenshots/product-detail.png)

<a name="reviews"></a>
### Reviews

- Only a customer who has genuinely bought a product can review it — reviews can't be faked by someone who never purchased
- One review per customer per product, editable or deletable at any time by whoever wrote it
- Every new or edited review starts as pending and only becomes publicly visible once a staff member approves it from a dedicated moderation queue
- Approved, featured reviews are pulled onto the homepage automatically as customer testimonials

![Product reviews](docs/screenshots/product-reviews.png)
![Staff review moderation queue](docs/screenshots/review-moderation.png)

<a name="basket--checkout"></a>
### Basket & Checkout

- A basket that works for guests via their session, and automatically merges into their account the moment they log in, so nothing added before logging in is lost
- Live quantity updates, line totals, and a running basket total, with a clear progress indicator toward free delivery
- Secure checkout handled entirely by Stripe, supporting standard cards, 3D Secure authentication, and correctly handling declined payments without creating a broken order
- A genuine order confirmation page and email, generated only once Stripe has actually confirmed payment server-side via a webhook, not merely because the customer's browser reached a "success" URL

![Basket](docs/screenshots/basket.png)
![Checkout](docs/screenshots/checkout.png)
![Order confirmation](docs/screenshots/checkout-success.png)

<a name="user-accounts"></a>
### User Accounts

- Full account registration with mandatory email verification before login is allowed, and a secure password reset flow — every one of these pages is custom-styled to match the brand, not left as django-allauth's bare default templates
- A My Account page for managing saved delivery details, so returning customers never have to retype their address
- A complete order history, with a one-click **Reorder** button that adds every available item from a past order back into the basket, automatically skipping anything since discontinued or sold out rather than failing the whole action
- A personal wishlist, addable and removable from any product card, with logged-out visitors prompted to log in rather than the action failing silently

![Login](docs/screenshots/login.png)
![Sign up](docs/screenshots/signup.png)
![My Account](docs/screenshots/my-account.png)
![Order history](docs/screenshots/order-history.png)
![Wishlist](docs/screenshots/wishlist.png)

<a name="staff-tools"></a>
### Staff Tools

- A dedicated staff dashboard, reachable only by staff accounts, linking to every management tool in one place
- Full product management — add, edit, and deactivate products, including managing multiple photos and variants together on a single page — entirely from the live site, with no need to touch the Django admin
- Full category management, including add, edit, and delete
- A genuine safety rule, not just a convenience: a product or category that has ever appeared in a real customer order **cannot** be permanently deleted, only deactivated, so order history can never be silently destroyed by an accidental click

![Staff dashboard](docs/screenshots/staff-dashboard.png)
![Staff product list](docs/screenshots/staff-product-list.png)
![Staff product add/edit form](docs/screenshots/staff-product-form.png)

<a name="marketing--seo"></a>
### Marketing & SEO

- A dynamically generated `sitemap.xml` listing every product, category, and static page, and a `robots.txt` that always references the correct live host
- A genuinely unique, accurate title and meta description on every single page of the site, including every step of the login and password reset flow, with zero duplicated or placeholder text anywhere
- A custom, branded 404 page with a working search box and clear navigation, rather than Django's bare default error page
- A custom favicon matching the site's own brand mark, visible in the browser tab and as a home-screen icon on mobile
- A cookie consent banner, remembered across visits once dismissed
- A real newsletter signup with double confirmation: a genuine email is sent, and the subscription only activates once the link inside it is clicked

![Custom 404 page](docs/screenshots/404-page.png)

<a name="future-features"></a>
### Future Features

Documented honestly as deliberate scope decisions, not oversights:

- **Guest checkout** — checkout currently requires an account, a deliberate choice for this version to keep order history and reordering reliable, but a true guest checkout path is a natural next step
- **Multi-currency support** — currently priced in USD only
- **Product recommendations** — a "customers also bought" section on the product detail page
- **Wishlist sharing** — letting a customer share their wishlist with someone else, useful for gift-giving
- **A richer staff analytics dashboard** — sales trends and stock alerts, beyond the current product/category management tools

---

