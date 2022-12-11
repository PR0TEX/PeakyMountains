package org.example;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.List;

public class Main {

    private static final String chromedriverPath = "I:\\Instalki\\selenium_jars_and_drivers\\chromedriver/chromedriver.exe";
    private static final String baseUrl = "http://localhost:8001/pl/";
    private static final boolean guestMode = true;
    private static final String userMail = "jan.kowalski@gmail.com";

    public static void main(String[] args) throws InterruptedException {
        System.setProperty("webdriver.chrome.driver", chromedriverPath);
        ChromeOptions ops = new ChromeOptions();
        ops.addArguments("--disable-notifications");
        ops.addArguments("start-maximized");
        WebDriver webDriver = new ChromeDriver(ops);
        //go to URL of presta on localhost
        webDriver.get(baseUrl);
        buyingTest(webDriver);
        checkStatus(webDriver);
        webDriver.quit();
    }

    private static void register(WebDriver webDriver) {
        //click log-in button
        webDriver.findElement(By.id("_desktop_user_info")).findElement(By.cssSelector("a[rel='nofollow']")).click();
        //click register link
        webDriver.findElement((By.cssSelector("a[href='" + baseUrl + "logowanie?create_account=1']"))).click();
        fillPersonalData(webDriver);
        webDriver.findElement(By.id("field-password")).sendKeys("prestashop_demo");
        webDriver.findElement(By.id("field-birthday")).sendKeys("1970-05-31");
        //continue
        webDriver.findElement(By.cssSelector("button[data-link-action='save-customer']")).click();
    }

    private static void logIn(WebDriver webDriver) {
        //click log-in button
        webDriver.findElement(By.id("_desktop_user_info")).findElement(By.cssSelector("a[rel='nofollow']")).click();
        //fill in the mail
        webDriver.findElement(By.id("field-email")).clear();
        webDriver.findElement(By.id("field-email")).sendKeys(userMail);
        //fill in the password
        webDriver.findElement(By.id("field-password")).clear();
        webDriver.findElement(By.id("field-password")).sendKeys("prestashop_demo");
        //click the button to continue
        webDriver.findElement(By.id("submit-login")).click();
    }

    private static void checkStatus(WebDriver webDriver) {
        //copy order number
        String orderReference = webDriver.findElement(By.id("order-reference-value")).getText();
        String orderNumber = orderReference.split(":")[1].trim();
        //go into my account
        webDriver.findElement(By.className("account")).click();
        //go into history of orders
        webDriver.findElement(By.id("history-link")).click();
        //get status
        WebElement tbody = webDriver.findElement(By.tagName("tbody"));
        List<WebElement> ordersNumber = tbody.findElements(By.cssSelector("th[scope='row']"));
        List<WebElement> ordersStatus = tbody.findElements(By.tagName("span"));
        int index = 0;
        for (int i = 0; i < ordersNumber.size(); i++) {
            if (orderNumber.equals(ordersNumber.get(i).getText())) {
                index = i;
            }
        }
        System.out.println(ordersStatus.get(index).getText());
    }

    private static void buyingTest(WebDriver webDriver) throws InterruptedException {
        Thread.sleep(1000);
        int limitOfProductToCart = 5;
        buyElementsFromCategory(webDriver, 0, limitOfProductToCart);
        buyElementsFromCategory(webDriver, 1, limitOfProductToCart);
        //go into cart
        webDriver.findElement(By.id("_desktop_cart")).findElement(By.tagName("a")).click();
        //remove first product from cart
        removeFromCart(webDriver);
        goThroughCart(webDriver);
    }

    private static void buyElementsFromCategory(WebDriver webDriver, int categoryNumber, int limitOfProductToCart) throws InterruptedException {
        //get categories list
        List<WebElement> categories = webDriver.findElement(By.cssSelector("ul[id='top-menu']")).findElements(By.cssSelector("a[data-depth='0']"));
        //go to tab
        categories.get(categoryNumber).click();
        //go into product
        for (int i = 0; limitOfProductToCart > 0; limitOfProductToCart--, i++) {
            //go to product
            webDriver.findElement(By.id("js-product-list")).findElements(By.className("product-description")).get(i).findElement(By.tagName("a")).click();
            //add product to cart
            increaseQuantityAndAddElementToCart(webDriver, i);
            //get back to product list -> get categories list
            categories = webDriver.findElement(By.cssSelector("ul[id='top-menu']")).findElements(By.cssSelector("a[data-depth='0']"));
            //go to category
            categories.get(categoryNumber).click();
        }
    }

    private static void addElementToCart(WebDriver webDriver) throws InterruptedException {
        //add to cart
        webDriver.findElement(By.className("add-to-cart")).click();
        //wait for element to show
        Thread.sleep(2000);
        //continue shopping button
        webDriver.findElement(By.className("cart-content-btn")).findElement(By.className("btn-secondary")).click();
        //wait for element to hide
        Thread.sleep(2000);
    }

    private static void increaseQuantityAndAddElementToCart(WebDriver webDriver, int quantity) throws InterruptedException {
        //increase quantity
        for(int i = 0; i < quantity % 3; i++) {
            webDriver.findElement(By.className("touchspin-up")).click();
        }
        List<WebElement> sectionsCustomizations = webDriver.findElements(By.cssSelector("section[class='product-customization js-product-customization']"));
        if (sectionsCustomizations.size() > 0) {
            WebElement textarea = sectionsCustomizations.get(0).findElement(By.cssSelector("textarea[class='product-message']"));
            textarea.clear();
            textarea.sendKeys("BE PROJECT");
            sectionsCustomizations.get(0).findElement(By.cssSelector("button[class='btn btn-primary float-xs-right']")).click();
        }
        addElementToCart(webDriver);
    }

    private static void removeFromCart(WebDriver webDriver) {
        webDriver.findElements(By.className("remove-from-cart")).get(0).click();
    }

    private static void goThroughCart(WebDriver webDriver) throws InterruptedException {
        //place order
        webDriver.findElement(By.className("cart-summary")).findElement(By.className("btn-primary")).click();
        if (guestMode) {
            //fill in personal data
            fillPersonalData(webDriver);
            //fill in password field
            webDriver.findElement(By.id("field-password")).sendKeys("prestashop_demo");
            //fill in birthdate field
            webDriver.findElement(By.id("field-birthday")).sendKeys("1970-05-31");
            //continue
            webDriver.findElement(By.cssSelector("button[data-link-action='register-new-customer']")).click();
        }
        //fill in address fields
        fillAddress(webDriver);
        //choose delivery option
        chooseDeliveryOption(webDriver);
        //accept conditions and place an order
        choosePayingMethodAcceptConditionsAndPlaceAnOrder(webDriver);
    }

    private static void fillPersonalData(WebDriver webDriver) {
        //choose gender
        webDriver.findElement(By.id("field-id_gender-1")).click();
        //input name
        webDriver.findElement(By.id("field-firstname")).sendKeys("Jan");
        //input surname
        webDriver.findElement(By.id("field-lastname")).sendKeys("Kowalski");
        //email field-email
        webDriver.findElement(By.id("field-email")).sendKeys(userMail);
        //checkboxes
        webDriver.findElement(By.cssSelector("input[name='customer_privacy']")).click();
        webDriver.findElement(By.cssSelector("input[name='psgdpr']")).click();
    }

    private static void fillAddress(WebDriver webDriver) {
        //input address
        webDriver.findElement(By.id("field-address1")).sendKeys("Do Studzienki");
        //input postcode
        webDriver.findElement(By.id("field-postcode")).sendKeys("80-227");
        //input city
        webDriver.findElement(By.id("field-city")).sendKeys("Gdańsk");
        //continue
        webDriver.findElement(By.cssSelector("button[name='confirm-addresses']")).click();
    }

    private static void chooseDeliveryOption(WebDriver webDriver) throws InterruptedException {
        //choose delivery option
        List<WebElement> deliveryOptions = webDriver.findElement(By.className("delivery-options")).findElements(By.className("js-delivery-option"));
        deliveryOptions.get(0).click();
        Thread.sleep(1000);
        deliveryOptions.get(2).click();
        //add comment
        webDriver.findElement(By.id("delivery_message")).sendKeys("Proszę o jak najszybszą realizację. Dziękuję :)");
        //continue
        webDriver.findElement(By.cssSelector("button[name='confirmDeliveryOption']")).click();
    }

    private static void choosePayingMethodAcceptConditionsAndPlaceAnOrder(WebDriver webDriver) throws InterruptedException {
        //paying method
        webDriver.findElement(By.cssSelector("label[for='payment-option-3']")).click();
        //accept
        webDriver.findElement(By.id("conditions_to_approve[terms-and-conditions]")).click();
        Thread.sleep(1500);
        //place an order
        webDriver.findElement(By.id("payment-confirmation")).findElement(By.className("btn-primary")).click();
    }

}