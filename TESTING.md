# Testing

This document covers how AfroMart has been tested: an automated suite covering models, forms, and views across every app, followed by manual testing, accessibility and code validation, and Lighthouse performance auditing.

## Automated Tests

Every app has a full `tests.py` file. There is no separate testing framework beyond Django's own `TestCase`, which is the standard, well-documented approach for a Django project and needs no extra setup beyond what's already in requirements.txt.

### Running the suite

```bash
python manage.py test
```

This creates a temporary throwaway test database, runs every test against it, and destroys it afterwards, so it never touches real development or production data. Django also automatically swaps in a local, in-memory email backend for the duration of the run, so no real emails are sent while testing the contact form, review notifications, order confirmations, or newsletter signup.

A clean run currently reports:
Found 116 test(s).
Ran 116 tests in 63.6s


### What each test class actually verifies

The table below maps every test class back to the specific user story or issue it was written to prove, rather than just listing test names with no context. This is deliberate: a test suite that exists but cannot be tied back to a requirement does not actually demonstrate the site meets that requirement, it just demonstrates that some code runs.

**core app**

| Test class | Verifies |
|---|---|
| `StaticPageTests` | Every static page (home, our story, terms, privacy, delivery and returns, FAQ) loads correctly and uses its own real template — issue #30 (every page reachable) and issue #32 (accurate titles and descriptions on every page) |
| `RobotsTxtTests` | robots.txt is served as plain text and correctly names the sitemap using the real host — issue #37 |
| `ContactFormTests` | The contact form sends a genuine email with the customer's address set as reply-to, and correctly re-shows the form with an error rather than silently failing when a required field is missing — issue #36 |

**products app**

| Test class | Verifies |
|---|---|
| `CategoryModelTests`, `ProductModelTests` | Slugs and SKUs generate automatically and never collide, stock correctly reflects availability, and `primary_image` correctly prefers the image staff marked as primary, falling back sensibly when none is marked or none exist at all |
| `ProductQuerySetTests` | Search matches against name and description, price filtering works correctly, and only active, featured products appear in the featured list — supports issue #11 (browse by category) and issue #13 (filter by price range) |
| `ReviewFormTests`, `ProductFormTests`, `CategoryFormTests` | Each form accepts valid data and correctly rejects invalid data (out-of-range ratings, missing required fields, duplicate category names) |
| `ProductListViewTests`, `ProductDetailViewTests` | Inactive products never appear in listings or search results, category filtering works, and an unknown product slug returns a proper 404 rather than an error page |
| `ReviewWorkflowTests` | The full review lifecycle: only someone who has actually bought the product can review it, one review per customer per product, editing a review resets it to unapproved, and nobody can edit or delete someone else's review — issues #25, #26, #27 |
| `ReviewModerationViewTests` | Only staff can reach the moderation queue (anonymous and regular users both get a 403), and approving or rejecting a review works correctly — issue #27 |
| `StaffProductManagementTests` | Non-staff cannot reach any staff product tool, staff can add and edit products including photos and variants together, and a product or category tied to real order history is protected from deletion — issue #29. Also includes a regression test for a real bug found while building this suite, where two inline formsets on the same page shared one default prefix and silently dropped rows past whichever formset's row count was shorter |

**basket app**

| Test class | Verifies |
|---|---|
| `BasketModelTests` | Line totals correctly include variant price adjustments, and the free-delivery threshold is calculated correctly at, above, and below the cutoff |
| `BasketServiceTests` | A guest's basket persists across requests via their session, a logged-in user's basket is tied to their account instead, and a guest basket correctly merges into their account the moment they log in |
| `BasketViewTests` | Adding, updating, and removing basket items all work correctly, a quantity above available stock is rejected, and one visitor can never modify another visitor's basket item by guessing its ID — issue #16, #17, #18. Also covers a real bug this suite found: posting a quantity of exactly 0 was being silently treated as invalid input and reset to 1, instead of being treated as the deliberate "remove this item" signal it's meant to be |

**checkout app**

| Test class | Verifies |
|---|---|
| `OrderModelTests` | Order numbers generate automatically and never collide, and totals calculate correctly both above and below the free-delivery threshold |
| `OrderFormTests` | The checkout address form correctly rejects a missing required field |
| `CreateOrderFromBasketTests` | A basket correctly becomes a real order with matching line items, and critically, that the price a customer paid is locked in at the moment of purchase and does not change even if the product's price changes afterwards |
| `CheckoutViewTests` | A logged-out visitor is redirected to log in rather than allowed to check out as a guest, an empty basket cannot proceed to checkout, and a valid submission creates a real order and shows the Stripe payment page |
| `CheckoutSuccessViewTests` | A customer can view their own order confirmation, but never someone else's, even by guessing the order number |
| `WebhookHandlerTests` | A confirmed Stripe payment correctly moves the order to Processing and sends one confirmation email, an order number Stripe doesn't recognise is handled gracefully rather than crashing, and critically, that Stripe redelivering the same successful-payment event a second time (which Stripe explicitly documents it can do) never results in a second confirmation email — issue #21 |

**profiles app**

| Test class | Verifies |
|---|---|
| `UserProfileModelTests`, `ProfileFormTests` | The profile form has no required fields (so a brand new customer's My Account page never errors), and saves correctly when filled in — issue #10 |
| `WishListModelTests`, `WishlistViewTests` | A product can only appear once per wishlist, the page requires login, toggling correctly adds and removes items, a logged-out AJAX request gets a proper 401 with a login link rather than failing silently, and one user never sees another user's wishlist items — issue #24 and the login-gating rule from issue #9 |
| `MyAccountViewTests` | A profile is created automatically on first visit, and submitting the form saves the new details — issue #10 |
| `OrderHistoryViewTests` | The page requires login and only ever shows the logged-in user's own orders, never anyone else's — issue #22 |
| `ReorderViewTests` | Reordering correctly skips products that have since been discontinued or gone out of stock rather than failing the whole action, and one user can never reorder someone else's past order |

**marketing app**

| Test class | Verifies |
|---|---|
| `NewsletterSubscriberModelTests`, `NewsletterSignupFormTests` | The model and form behave correctly with valid and invalid email addresses |
| `NewsletterSignupViewTests` | A new signup gets a real, unsent-until-confirmed subscription with a genuine confirmation email, an already-confirmed address isn't signed up twice, and an already-pending address doesn't get a second confirmation email |
| `ConfirmSubscriptionViewTests` | A valid confirmation link correctly confirms the subscription, and an unknown token returns a proper 404 |