# Testing
A comprehensive testing strategy was essential for this project. It combines manual testing of all user stories and funcitonality with automated tests to ensure code reliability and data integrity. This approach guarantees a robust and user-friendly application.

## Table of Contents
* [Validation](#validation)
* [Lighthouse](#lighthouse)
* [Responsiveness](#responsiveness)
* [Browser Compatibility](#browser-compatibility)
* [Automated Testing](#automated-testing)
* [Manual Testing](#manual-testing)
* [User Stories](#user-stories)
* [Bugs](#bugs)


## Validation
### HTML
- To validate all HTML files, the recommended validator service by Code Institute which is [HTML Validator](https://validator.w3.org/) was used.

<details>
 
**<summary> View HTML Code Validation </summary>**

| Validation URL used      | Comment   | Screenshot         |  |
| --------- | --------- | ------------------ | ------ |
|  https://floral-fantasy-bcd2bd74ac5e.herokuapp.com/     | No Errors | ![](documentation/testing/html-floral-fantasy.png) |  |

</details>

### CSS
- To validate the CSS file, the recommended validator service by Code Institute which is [CSS Validator](https://jigsaw.w3.org/css-validator/) was used.

<details>
 
 **<summary> View CSS Code Validation </summary>**

| File                                          | Comment  | Screenshot                                    |
| -------------------------------------------------- | -------- | --------------------------------------------- |
| **CSS Static** | No Error | ![](documentation/testing/css-static.png) |
| **profile.css** | No Error | ![](documentation/testing/css-profile.png) |
| **checkout.css** | No Error | ![](documentation/testing/css-checkout.png) |

</details>

### JavaScript
- To validate the JavaScript file, the recommended validator service by Code Institute which is [JSHint](https://jshint.com/) was used.

<details>
 
 **<summary> View JavaScript Code Validation </summary>**

| File                                          | Comment  | Screenshot                                    |
| -------------------------------------------------- | -------- | --------------------------------------------- |
| **Static JS Navbar** | No Error | ![](documentation/testing/js-static-navbar.png) |
| **JS checkout** | No Error | ![](documentation/testing/js-checkout.png) |


</details>

### Python
- To validate Python code, the recommended validator service by Code Institute which is [Python PEP8 Checker](https://ww7.pep8online.com/?usid=24&utid=12257950545) was used.

<details>
 
 **<summary> View Python Code Validation </summary>**

| File              | Comment | Screenshot         |
| ----------------- | ------- | ------------------ |
| **floral_fantasy**   |         |                    |
| **settings.py**    | *Line exceeds recommended length; left as-is for readability and to avoid further warnings *        | ![](documentation/testing/settings.png) |
| **Cart**   |         |                    |
| **views.py**        |    **     | ![](documentation/testing/python-cart.png) |
| **Checkout** |         |                    |
| **admin.py**      |    No error     | ![](documentation/testing/python-checkout-admin.png) |
| **forms.py**      |    No error     | ![](documentation/testing/python-checkout-forms.png) |
| **models.py**     |    **     | ![](documentation/testing/python-checkout-models.png)|
| **test.py**     |    No error     | ![](documentation/testing/python-checkout-test.png)|
| **views.py**      |    **     | ![](documentation/testing/python-checkout-view.png) |
| **Landing/HomePage** |         |                    |
| **test.py**      |    **     | ![](documentation/testing/python-landing-test.png) |
| **views.py**      |    No error     | ![](documentation/testing/python-landing-views.png) |
| **Products** |         |                    |
| **models.py**      |    No error     | ![](documentation/testing/python-product-models.png) |
| **views.py**      |    **     | ![](documentation/testing/python-product-views.png) |
| **Profile** |         |                    |
| **models.py**      |    **     | ![](documentation/testing/python-profile-models.png) |
| **test.py**      |    **     | ![](documentation/testing/python-profile-test.png) |
| **views.py**      |    **     | ![](documentation/testing/python-profile-view.png) |

 </details>

[Back To Top](#table-of-contents)

## Lighthouse
- For auditing Performance, Accessibility, and Best Practices [Developer Tools Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/) was used.

 <details>
 
 **<summary> View Lighthouse Testing </summary>**

| Device      | Page         | Screenshot                                   |
| ----------- | ------------ | -------------------------------------------- |
| **Desktop** | Home         | ![](documentation/testing/) |
| **Mobile**  | Home         | ![](documentation/testing/) |
| **Desktop** | Products         | ![](documentation/testing/) |
| **Mobile**  | Products         | ![](documentation/testing/) |
| **Desktop** | Product Details | ![](documentation/testing/) |
| **Mobile**  | Product Details | ![](documentation/testing/) |
| **Desktop** | Cart   | ![](documentation/testing/) |
| **Mobile**  | Cart   | ![](documentation/testing/) |
| **Desktop** | Checkout | ![](documentation/testing/) |
| **Mobile**  | Checkout | ![](documentation/testing/) |
| **Desktop** | Profile         | ![](documentation/testing/) |
| **Mobile**  | Profile         | ![](documentation/testing/) |

 </details>

## Responsiveness
- The application was tested to ensure it will respond correctly on desktop, tablet, and mobile devices, maintaining usability and layout integrity.
<details>
 
 **<summary>View Responsiveness Screenshot on Different Devices</summary>**

| Device      | Comment | Screenshot             |
| ----------- | ---------| ------------- |
| **20" Desktop 1600x900** |  [ResponsiveChecker](https://responsivedesignchecker.com/)  |![home](documentation/testing/responsiveness-home-desktop.png) |
| **Laptop 1024x868**  |   Chrome(devtools)     | ![home](documentation/testing/responsiveness-laptop.png) |
| **15" Notebook 1366x768**  |   [ResponsiveChecker](https://responsivedesignchecker.com/)     | ![home](documentation/testing/responsiveness-15notebook.png) |
| **iPad Mini 768x1024**  | [ResponsiveChecker](https://responsivedesignchecker.com/)   | ![home](documentation/testing/responsiveness-ipad-mini.png) |
| **Samsung Galaxy Tab10 800x1280**  | [ResponsiveChecker](https://responsivedesignchecker.com/)       | ![home](documentation/testing/responsiveness-samsung-galaxy.png) |
| **iPhone 414x736**  |  [ResponsiveChecker](https://responsivedesignchecker.com/)      | ![home](documentation/testing/responsiveness-iphone.png) |
| **Mobile 425x651**  |   Chrome(devtools)     | ![home](documentation/testing/responsiveness-chrome-mobile.png) |


</details>

## Browser Compatibility
- The application was tested for basic compatibility on major browsers including Chrome, Firefox, MS Edge and Opera. Core functionality and layout appeared consistent across these browsers.

<details>
 
 **<summary>View Compatibility Screenshot on Different Browser</summary>**

| Browser     | Comment | Screenshot             |
| ----------- | ------- | ---------------------- |
| **Chrome**  |   Performs as intended      | ![home](documentation/testing/browser-comp-chrome.png) |
| **Firefox** |   Performs as intended      | ![home](documentation/testing/browser-comp-firefox.png) |
| **MS Edge** |   Performs as intended      | ![home](documentation/testing/browser-comp-edge.png) |
| **Opera**   |   Performs as intended      | ![home](documentation/testing/browser-comp-opera.png) |

</details>

[Back To Top](#table-of-contents)

## Automated testing
Automated test help ensure reliability and support continuous integration by checking that models, views, and other components work as expected. 

<details>
 
 **<summary>View Automated Testing</summary>**

| Apps/File     | Comment | Screenshot             |
| ----------- | ------- | ---------------------- |
| **Cart**  |   Performs as intended      | ![home](documentation/testing/automated-cart-testing.png) |
| **Checkout** |   Performs as intended      | ![home](documentation/testing/automated-checkout-testing.png) |
| **Landing/Home** |   Performs as intended      | ![home](documentation/testing/automated-landing-testing.png) |
| **Products**   |   Performs as intended      | ![home](documentation/testing/automated-products-testing.png) |
| **Profile**   |   Performs as intended      | ![home](documentation/testing/automated-profile-testing.png) |
| **Webhook**   |   Performs as intended      | ![home](documentation/testing/automated-webhook-testing.png) |

</details>

### Stripe/Webhook
Stripe webhooks allow the application to receive real-time notifications for events like payments and updates. These were tested both locally using the Stripe CLI in the terminal and on the deployed applicaiton to ensure secure handling and proper synchronisation with Stripe.

<details>
 
 **<summary>View Stripe Testing</summary>**

| Testing     | Comment | Screenshot             |
| ----------- | ------- | ---------------------- |
| **Stripe CLI**  |        |  |
|  |         | ![](documentation/testing/terminal-pay-int-create.png) |
|  |   Performs as intended      | ![](documentation/testing/terminal-created.png) |
|  |         | ![](documentation/testing/terminal-pay-int-succeed.png) |
|  |   Performs as intended      | ![](documentation/testing/terminal-succeed.png) |
|  |         | ![](documentation/testing/terminal-pay-failed.png) |
|  |   Performs as intended      | ![](documentation/testing/terminal-failed.png) |
| **Events**   |   based on deployed App     |  |
|    |   Performs as intended      | ![](documentation/testing/stripe-testing5.png) |
|    |   Performs as intended      | ![](documentation/testing/stripe-testing6.png) |
|    |   Performs as intended      | ![](documentation/testing/stripe-testing7.png) |

</details>

[Back To Top](#table-of-contents)

## Manual Testing
All core features and user interactions of the application were manually tested to ensure proper funcitonality. This include checking buttons, forms, navigation, and workflows across the app to confirm that each component behaves as expected.

### Navbar
| Comment | Screenshot             |
| ------- | ---------------------- |
| **solid navbar** | ![](documentation/testing/navbar-solid.png) |
| **navbar** | ![](documentation/testing/navbar.png) |
| **logged in user** | ![](documentation/testing/navbar-loggedin-user.png) |
| **superuser** | ![](documentation/testing/navbar-superuser.png) |

| Action | Expected Result | Comment |
| --------------------- | -------------------------------------- | ---------------------------------------- |
| click on logo | should navigate to homepage | **Pass**- Achieves desired functionality |
| click on Home | should navigate to homepage | **Pass**- Achieves desired functionality |
| click on Products | should navigate to product list page | **Pass**- Achieves desired functionality |
| click on Cart Icon | should navigate to cart page | **Pass**- Achieves desired functionality |
| click on User Icon | (not logged in/new user) should have access to login/signup page | **Pass**- Achieves desired functionality |
| click on User Icon | (logged in user) should have access to profile/logout page | **Pass**- Achieves desired functionality |
| click on User Icon | (logged in superuser) should have access to profile/product control/logout page | **Pass**- Achieves desired functionality |
| click on Sign Up | should navigate to signup page | **Pass**- Achieves desired functionality |
| click on Log In | should navigate to login page | **Pass**- Achieves desired functionality |
| click on My Profile | should navigate to user's dashboard | **Pass**- Achieves desired functionality |
| click on Log Out | logged out and redirect to log in page | **Pass**- Achieves desired functionality |

### Footer

![](documentation/testing/footer.png)
| Action | Expected Result | Comment |
| ----------------------- | ---------------------------------------------------------- | ---------------------------------------- |
| click on Facebook Icon | should navigate to the facebook page in a separate window | **Pass**- Achieves desired functionality |
| click on Instagram Icon | should navigate to the instagram page in a separate window | **Pass**- Achieves desired functionality |
| click on X Icon | should navigate to the x page in a separate window | **Pass**- Achieves desired functionality |

### Landing Page Buttons
| Comment | Screenshot             |
| ------- | ---------------------- |
| **Shop Now button** | ![](documentation/testing/home-btn.png) |
| **Shop Now button** | ![](documentation/testing/home-btn2.png) |
| **Submit button** | ![](documentation/testing/home-btn3.png) |

| Action                                     | Expected Result                             | Comment                                  |
| ------------------------------------------ | ------------------------------------------- | ---------------------------------------- |
| click on Shop Now                      | should navigate to Product Listing page        | **Pass**- Achieves desired functionality |
| click on Submit               | should submit the forms             | **Pass**- Achieves desired functionality |

### Products Page
| Comment | Screenshot             |
| ------- | ---------------------- |
| **Products Page** | ![](documentation/testing/products-page.png) |
|  | ![](documentation/testing/products-page2.png) |


| Action                                     | Expected Result                             | Comment                                  |
| ------------------------------------------ | ------------------------------------------- | ---------------------------------------- |
| click on Product Item                      | should navigate to Product details page        | **Pass**- Achieves desired functionality |
| click on Sort by                      | should sort the products by price(low-high, high-low) or alphabetical        | **Pass**- Achieves desired functionality |
| click on Search                      | user can search products, clicking the search icon with no text shows all items.        | **Pass**- Achieves desired functionality |
| click on Edit|Delete                      | should give the superuser an access to edit or delete an item  | **Pass**- Achieves desired functionality |
| click on Prev or Next                      | should navigate to previous page or next page        | **Pass**- Achieves desired functionality |

### Products Details Page
### Cart Page
### Checkout Page
### My Profile Page
### SignUp Form
### Contact Form
### LogIn Page
### LogOut Page
### Reset Password Page

[Back To Top](#table-of-contents)

## User Stories

## Bugs
[Back To Top](#table-of-contents)