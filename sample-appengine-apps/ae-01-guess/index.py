import sys

print 'Content-Type: text/html'
print ''
print '<pre>'

# Read the form input which is a single line as follows
# guess=42
data = sys.stdin.read()
# print data
try:
   guess = int(data[data.find('=')+1:])
except:
   guess = -1

# Code for the lesson

print 'Your guess is', guess

answer = 42

if guess < answer :
   print 'Your guess is too low'

if guess == answer:
   print 'Congratulations!'

if guess > answer :
   print 'Your guess is too high'

# End of the lesson code

print '</pre>'

print '''<form method="post" action="/">
<p>Enter Guess: <input type="text" name="guess"/></p>
<p><input type="submit"></p>
</form>'''
