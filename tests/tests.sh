#!/bin/bash
set -e
. assert.sh
# Check whether we are getting correct output or not
assert "blog post add 1 1 " "post_content : 1\npost_title: 1\nPost Added"
# Check whether we are getting correct exit code or not
assert_raises "blog post list" 0
assert "blog post add 1 1 -C 1" "post_content : 1\npost_title: 1\nPost Added\nCatogry assigned to post"
assert_raises "blog post search 1" 0
assert "blog category add 1  " "name : 1"
assert_raises "blog category list" 0
assert_raises "blog category assign 1" 0
# end of test suite
assert_end examples

