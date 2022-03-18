## **WHICH PLANE IS FLEWING OVER YOUR HOUSE?**

Have you ever wondered which plane flew over your house? 
I did.   

You may be wondering why I do this. Because I can.

-----------

**SETUP LIBRARIES**

Open a new terminal and run this command sentence by sentence 

------------

    $ pip3 install selenium

    $ pip3 install bokeh

    $ pip3 install geckodriver-autoinstaller

    $ sudo apt-get install chromium-chromedriver

    $ pip3 install pandas

    $ pip3 install beautifulsoup4

    $ pip3 install numpy --upgrade

------------------
**USING CODES**

Open main.py file 

(dont touch url_image_save.py file, it is just library that i coded for scrapping photos from https://www.jetphotos.com/)

Change line 14 and line 15 according to your location, and line 16 you can change threshold (it means radius). Default is 1 but it is so big value, i just used it for test purposes.
In real life you can set it to **0.03** or 0.05. Don't make it too small.

-----------

For getting plane registration we need to use Airlabs API. So you can get API KEY from here: https://airlabs.co/     
I suggest use temp mails.
Change the line 18 with your **Airlabs API KEY**

---------


Check this link for creating bot and chat id:

https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e

When you get **Telegram Bot** "**key**" and "**bot chat id**" change line 21 and line 22 with them.

------

**TEST VIDEO**

https://user-images.githubusercontent.com/81293327/159037270-a1c50b7c-c509-4cd6-a18a-07218b738cd1.mp4


Tested with Raspberry Pi 4 

