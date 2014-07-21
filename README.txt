Hello and welcome to the California Report Card team! 

This document is here to guide you through setting up the CRC on your local machine
and also give you an overview of how to change the files. 

Important files: 
Location File                    Name                  Purpose
src\server\opinion\templates     mobile.html           Here is where the entire website is laid out. 

src\server\opinion               settings_local.py     Default settings and text replacement gets set
                                                       here!

src\server\opinion\opinion_core  models.py             Where the DiscussionStatement and other useful
                                                       Django models are defined

src\server\opinion\includes      queryutils.py         Commonly used queries - format_general_discussion_comment function 

src\server\opinion\templates     search.html           All function relating to loading all the user comments

Change log:
opinion_core/models.py
    Added fields to DiscussionComment class 
        -added spanish_comment - Spanish version of an English comment 
        -added original_language - Original language that the comment was written in - either "english" or "spanish"
        -changed the SQL database to reflect these changes 
    Added fields to OpinionSpaceStatement class
        -added spanish_statement - Spanish version of an English statement
        -input type - the form of user input. For example, "slider" or "textbox"
Updated query_utils 
    -format_general_discussion_comment
Updated search.html 
    -updated populate_table added two table elements - spanish_comment and original_language
    -changed table headers (in HTML) at the bottom of the file for the header
    -added allowSpanishCommentEditing function which acts like allowCommentEditing() and called it in getSearchResults().
    -changed both commentEditing functions to pass an additional parameter language as part of the request. 
Updated views.py
    -changed mobile function return value with a added key "spanish" with the value of a boolean (this is for later in mobile.html so that we can decide which language we are going to use). determined type of variable through parsing argument that will be providing in html of california report card
    -proof_read_comments - added a variable language that tracks which language the comment we are editing is in. 


Questions:
1. How do we store the two languages as two different tables?