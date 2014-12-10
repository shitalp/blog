#!/bin/bash
set -e

. assert.sh
# Check whether we are getting correct output or not
assert "./blog.py post add 1 1 " "post_content : 1\npost_title: 1\nPost Added"
# Check whether we are getting correct exit code or not
assert_raises "./test.py post list" 0
assert "./blog.py post add 1 1 -C 1" "post_content : 1\npost_title: 1\nPost Added\nCatogry assigned to post"
assert_raises "./test.py post search 1" 0
assert "./blog.py category add 1  " "name: 1"
assert_raises "./blog.py category list" 0
assert_raises "./blog.py category assign 1" 0
# end of test suite
assert_end examples

