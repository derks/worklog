WorkLog
========

Start an activity
::

	$ wl start playing chess

Pause it with a random encounter
::

	$ wl end fapping

Check out how long did the fapping take you
::

	$ wl diff
	2012-07-11 10:09:23.626468 end    fapping
	diff: 0:00:12.802342

Resume what you have started
::

	$ wl resume

Check out your logs since you have started
::

	$ wl end # <- this step shouldn't be needed in the future, before doing `diff -f`
	$ wl diff -f
	2012-07-11 10:09:09.823053 start  playing chess
	2012-07-11 10:09:23.626468 end    fapping
	2012-07-11 10:11:04.459657 resume
	2012-07-11 10:11:15.852227 end
	diff: 0:00:25.195985

List all your logs
::

	$ wl list
	2012-07-11 09:52:34.045907 start  fuuu
	2012-07-11 09:52:37.928545 end    kek
	2012-07-11 10:09:09.823053 start  playing chess
	2012-07-11 10:09:23.626468 end    fapping
	2012-07-11 10:11:04.459657 resume
	2012-07-11 10:11:15.852227 end

And wrap up
::

	$ wl pop
	2012-07-11 10:09:09.823053 start  playing chess
	2012-07-11 10:09:23.626468 end    fapping
	2012-07-11 10:11:04.459657 resume
	2012-07-11 10:11:15.852227 end
	diff: 0:00:25.195985
	$ wl list
	2012-07-11 09:52:34.045907 start  fuuu
	2012-07-11 09:52:37.928545 end    kek
