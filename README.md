# pingLoop
This script provides two methods of pinging domains, supposedly aiming to attack or boost their SEO rank. Attacking works by pinging random paths and boosting by just pinging provided paths. No results are quaranteed, it's a simple pinging tool. Detailed logging is provided on each script run, as well as IP rotation after each URL ping.

Use it to test and experiment with your website's behaviour and SEO rank.

**Mode A, SEO Attack:**

Random paths are added at the end of each provided URL. The request results in a 404 error response, if the website does not handle Not Found errors with a redirect (301). Script reads a list of provided URLs in a .xls or .xlsx file named "attack". User inputs the following:

a) How many different URLs to construct (random paths are added at the end of each  main URL, i.e. 'test.com/f983u4')
b) How many times to ping each unique randomly constructed URL.
c) Whether a script scheduling to rerun after it has finished is wanted or not. If yes, user needs to provide the time interval.

**Mode B, SEO Boost:**

Script reads a list of provided URLs in a .xls or .xlsx file named "boost". User just needs to input the number of times to ping each URL. 

**Environment Setup Instructions:**

In a Linux machine:

1) Install Tor and restart it

'sudo apt-get install tor'
'sudo /etc/init.d/tor restart'

2) Create a hashed password to prevent unauthorized port access from outside

'tor --hash-password <password>'

3) Change config file

'cd /etc/tor'
'sudo nano torrc'

-> Uncomment the following lines, so it looks like this:

SOCKSPort 9050
HashedControlPassword <your hashed passsword obtained earlier here>
CookieAuthentication 1

4)Save, exit and restart tor

'sudo /etc/init.d/tor restart'

5) Install tor requests wrapper and requests (python libraries)

'pip install torrequest'
'pip install request'


**_Disclaimer: This script was made solely for educational and testing purposes. Please test this bot on your own website/domain. I am not responsible for any misuse of this script._**
