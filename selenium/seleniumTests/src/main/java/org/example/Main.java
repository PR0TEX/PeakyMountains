package org.example;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.interactions.Actions;

import java.util.List;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        System.setProperty("webdriver.chrome.driver", "I:\\Instalki\\selenium_jars_and_drivers\\chromedriver/chromedriver.exe");
        WebDriver webDriver = new ChromeDriver();

        webDriver.manage().window().maximize();
        //go to URL of presta on localhost
        webDriver.get("http://localhost:8001/pl/");
        Thread.sleep(10000);
        //go to "clothes" tab (id=category-3)
        webDriver.findElement(By.cssSelector("a[href='http://localhost:8001/pl/3-clothes']")).click();
        //go to "Men" section
        webDriver.findElement(By.linkText("Men")).click();
        //go to product
        webDriver.findElement(By.cssSelector("a[href='http://localhost:8001/pl/men/1-1-hummingbird-printed-t-shirt.html#/1-rozmiar-s/8-kolor-bialy'")).click();
        addElementToCart(webDriver);
        //continue shopping button
        webDriver.findElement(By.className("cart-content-btn")).findElement(By.className("btn-secondary")).click();
        //wait for element to hide
        Thread.sleep(2000);
        //hover "clothes" tab
        hoverClothesTab(webDriver);
        //go to women section
        webDriver.findElement(By.cssSelector("a[href='http://localhost:8001/pl/5-women']")).click();
        //go to product
        webDriver.findElement(By.cssSelector("a[href='http://localhost:8001/pl/women/2-9-brown-bear-printed-sweater.html#/1-rozmiar-s'")).click();
        //increase quantity
        increaseQuantityAndAddElementToCart(webDriver);
        //go to order realisation
        webDriver.findElement(By.className("cart-content-btn")).findElement(By.className("btn-primary")).click();
        goThroughCartAsGuest(webDriver);

        //webDriver.close();
    }

    private static void addElementToCart(WebDriver webDriver) throws InterruptedException {
        //add to cart
        webDriver.findElement(By.className("add-to-cart")).click();
        //wait for element to show
        Thread.sleep(2000);
    }

    private static void increaseQuantityAndAddElementToCart(WebDriver webDriver) throws InterruptedException {
        //increase quantity
        webDriver.findElement(By.className("touchspin-up")).click();
        addElementToCart(webDriver);
    }

    private static void hoverClothesTab(WebDriver webDriver) throws InterruptedException {
        //hover "clothes" tab
        WebElement clothesTab = webDriver.findElement(By.cssSelector("a[href='http://localhost:8001/pl/3-clothes']"));
        Actions actions = new Actions(webDriver);
        actions.moveToElement(clothesTab).perform();
        Thread.sleep(1000);
    }

    private static void goThroughCartAsGuest(WebDriver webDriver) throws InterruptedException {
        //go into cart
        webDriver.findElement(By.cssSelector("a[href='http://localhost:8001/pl/zamówienie']")).click();
        //fill in personal data
        fillPersonalData(webDriver);
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
        webDriver.findElement(By.id("field-email")).sendKeys("jan.kowalski@gmail.com");
        //checkboxes
        webDriver.findElement(By.cssSelector("input[name='customer_privacy']")).click();
        webDriver.findElement(By.cssSelector("input[name='psgdpr']")).click();
        //continue
        webDriver.findElement(By.cssSelector("button[name='continue']")).click();
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
        System.out.println(deliveryOptions.size());
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