---
title: 'What’s different about the new Google Docs: Conflict resolution'
source: https://drive.googleblog.com/2010/09/whats-different-about-new-google-docs_22.html
author: Google
published: '2010-09-22'
site: Google Drive Blog
clipped: '2026-09-20'
---

# What’s different about the new Google Docs: Conflict resolution

Google Drive Blog
The latest news and updates from the Google Drive team.
What’s different about the new Google Docs: Conflict resolution
Wednesday, September 22, 2010
Editor’s note: This is the second in a series of three posts about the collaboration technology in Google Docs.
Yesterday
, we explained some of the technical challenges behind real time collaboration.
Think of the history of a document as a series of changes. In Google documents, all edits boil down to three basic types of changes: inserting text, deleting text, and applying styles to a range of text. We save your document as a revision log consisting of a list of these changes. When someone edits a document, they’re not modifying the underlying characters that represents the document. Instead they are appending their change to the end of the revision log. To display a document, we replay the revision log from the beginning.
To see what these changes look like, suppose that a document edited by John and Luiz initially reads;
EASY AS 123
. If John (represented by green) changes the document to
EASY AS ABC
, then he is making four changes:
Collaboration is not quite as simple as sending these changes to the other editors because people get out of sync. Suppose as John is typing, Luiz (represented by yellow) begins to change his document to
IT'S EASY AS 123
. He first inserts the
I
and the
T
at the beginning of the document:
Suppose Luiz naively applies John’s first change
{DeleteText @9-11}
:
He deleted the wrong characters! Luiz had two characters at the beginning of the doc that John was never aware of. So the location of John’s change was wrong relative to Luiz’s version of the document. To avoid this problem, Luiz must
transform
John’s changes and make them relative to his local document. In this case, when Luiz receives changes from John he needs to know to shift the changes over by two characters to adjust for the
IT
that Luiz added. Once he does this transformation and applies John’s first change, he gets:
Much better. The algorithm that we use to handle these shifts is called operational transformation (OT). If OT is implemented correctly, it guarantees that once all editors have received all changes, everyone will be looking at the same version of the document.
The OT logic in documents must handle all of the different ways that InsertText, DeleteText, and ApplyStyle changes can be paired and transformed against each other. The example above showed DeleteText being transformed against InsertText. To get a feel for how this works, here are a couple more examples of simple transformations:
Style ranges expand when they are transformed against text insertions:
{ApplyStyle bold @10-20}
transformed against
{InsertText 'ABC' @15}
results in
{ApplyStyle Bold @10-23}
.
Sometimes changes don’t conflict and there’s no need to transform anything. For example when a style change is transformed against a different type of style change, there is no conflict:
{ApplyStyle italic @10-20}
transformed against
{ApplyStyle font-color=red @0-30}
results in the same
{ApplyStyle italic @10-20}
because the range of text can be both red and italic simultaneously.
Collaboration in Google Docs consists of sending changes from one editor to the server, and then to the other editors. Each editor transforms incoming changes so that they make sense relative to the local version of the document. Tomorrow’s post will outline the protocol for deciding when each editor uses operational transformation.
Posted by: John Day-Richter, Software Engineer
Labels
#SafeOnline
accessibility
add-ons
Android
app scripts
apps
attachments
avery
back to school
blind
braille
charts
chat
Chrome
Chrome extensions
chrome web apps
Cloud Connect
collaboration
comments
community
discussions
docs
docs editors
document list
documents
documents list
drawings
Drive
drivebacktoschool
easybib
education
enterprise
Faces of Docs
folders
forms
gmail
gone google
Google Apps Blog
Google Apps Script
Google Cloud Connect
google docs
Google Docs Viewer
google documents
google drive
Google Drive Blog
Google Pack
Google Sites
Google+
googlenew
Guest Post
hangout on air
help
holiday
images
iOS
Keep
letterfeed
low-vision
mailchimp
mobile
nanowrimo
OCR
office compatibility mode
offline
paperless
pdfs
photo
photos
presentations
product ideas
profiles
quickoffice
Reddit
research
save to drive
screen reader
scripts
security
sharing
sheet
sheets
shortcut
slides
spell check
spreadsheets
stock photos
storage
students
suggested edits
tables
teachers
team
templates
videos
Viewer
work
Archive
2016
Sep
May
Apr
Feb
Jan
2015
Dec
Nov
Oct
Jul
Mar
Feb
Jan
2014
Dec
Nov
Oct
Sep
Aug
Jun
Apr
Mar
Jan
2013
Dec
Nov
Oct
Sep
Aug
Jun
May
Apr
Mar
Feb
Jan
2012
Dec
Nov
Oct
Sep
Aug
Jul
Jun
May
Apr
Mar
Feb
2011
Dec
Nov
Oct
Sep
Aug
Jul
Jun
May
Apr
Mar
Feb
Jan
2010
Dec
Nov
Oct
Sep
Aug
Jul
Jun
May
Apr
Mar
Feb
Jan
2009
Dec
Nov
Oct
Sep
Aug
Jul
Jun
May
Apr
Mar
Feb
Jan
2008
Dec
Nov
Oct
Sep
Aug
Jul
Jun
May
Apr
Mar
Feb
Jan
2007
Dec
Nov
Oct
Sep
Aug
Jul
Jun
May
Apr
Mar
Feb
Jan
2006
Dec
Nov
Oct
Feed
Visit our site
Google Drive
Google Docs, Sheets, Slides
Google
on
Follow @googledrive
Give us feedback in our
Product Forum
.
