---
title: Pastebin.com - Developers API
source: https://pastebin.com/doc_api
published: '2026-01-01'
site: Pastebin
clipped: '2026-09-20'
---

# Pastebin.com - Developers API

Looking for our Scraping API? 

    [Check out the Scraping API documentation](/doc_scraping_api).
Developers API

    
        This is the Pastebin.com developers API documentation page. Here you can find all the information you need to get started with our API. If you have questions, feel free to 

        
    
    
    [contact us](/contact). If you are a developer, and you are building something for Pastebin which might benefit others as well, be sure to contact us, as we might be able to feature your creation on our[tools page](/tools).
Your Unique Developer API Key

    
                    Everybody using our API is required to use a valid Developer API Key. You automatically get a key when you become a member of Pastebin.
            Please login to your account, and return to this page to find your Developer API Key.
        
    

    
    
    Creating A New Paste

    
        Creating a new paste via our API is very easy. You simply have to send a valid POST request to the url shown below.
        Please make sure you are sending the data 

as the UTF-8 charset.

    
    
    as the UTF-8 charset.

https://pastebin.com/api/api_post.php

        Below is a PHP example using curl how to create a new paste:
        $api_dev_key 			= 'YOUR API DEVELOPER KEY'; // your api_developer_key
$api_paste_code 		= 'just some random text you :)'; // your paste text
$api_paste_private 		= '1'; // 0=public 1=unlisted 2=private
$api_paste_name			= 'justmyfilename.php'; // name or title of your paste
$api_paste_expire_date 		= '10M';
$api_paste_format 		= 'php';
$api_user_key 			= ''; // if an invalid or expired api_user_key is used, an error will spawn. If no api_user_key is used, a guest paste will be created
$api_paste_name			= urlencode($api_paste_name);
$api_paste_code			= urlencode($api_paste_code);
$url 				= 'https://pastebin.com/api/api_post.php';
$ch 				= curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'api_option=paste&api_user_key='.$api_user_key.'&api_paste_private='.$api_paste_private.'&api_paste_name='.$api_paste_name.'&api_paste_expire_date='.$api_paste_expire_date.'&api_paste_format='.$api_paste_format.'&api_dev_key='.$api_dev_key.'&api_paste_code='.$api_paste_code.'');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_NOBODY, 0);
$response  			= curl_exec($ch);
echo $response;

        Below is a curl command example how to create a new paste:
    curl -X POST -d 'api_dev_key=YOUR API DEVELOPER KEY' -d 'api_paste_code=test' -d 'api_option=paste' "https://pastebin.com/api/api_post.php"

        Possible Good API Responses: (example)
        https://pastebin.com/UIFdu235s

        Possible Bad API Responses:
        Bad API request, invalid api_option
Bad API request, invalid api_dev_key
Bad API request, maximum number of 25 unlisted pastes for your free account
Bad API request, maximum number of 10 private pastes for your free account
Bad API request, api_paste_code was empty
Bad API request, maximum paste file size exceeded
Bad API request, invalid api_paste_expire_date
Bad API request, invalid api_paste_private
Bad API request, invalid api_paste_format
Bad API request, invalid api_user_key
Bad API request, invalid or expired api_user_key
Bad API request, you can't add paste to folder as guest

    Creating A New Paste, [Required Parameters]

    
        Include all the following POST parameters when you request the url:

1. api_dev_key - which is your unique API Developers Key.

2. api_option - set as paste, this will indicate you want to create a new paste.

3. api_paste_code - this is the text that will be written inside your paste.

Leaving any of these parameters out will result in an error.

    
    
    1. api_dev_key - which is your unique API Developers Key.

2. api_option - set as paste, this will indicate you want to create a new paste.

3. api_paste_code - this is the text that will be written inside your paste.

Leaving any of these parameters out will result in an error.

Creating A New Paste, [Optional Parameters]

    
        These parameters are not required when you create a new paste, but are possible to add:

1. api_user_key - this parameter is part of the login system, which is explained further down the page.

2. api_paste_name - this will be the name / title of your paste.

3. api_paste_format - this will be the syntax highlighting value, which is explained in detail further down the page.

4. api_paste_private - this makes a paste public, unlisted or private, public = 0, unlisted = 1, private = 2

5. api_paste_expire_date - this sets the expiration date of your paste, the values are explained futher down the page.

6. api_folder_key - this sets the key of the folder of your paste, the values are explained futher down the page.

        
    
    
    1. api_user_key - this parameter is part of the login system, which is explained further down the page.

2. api_paste_name - this will be the name / title of your paste.

3. api_paste_format - this will be the syntax highlighting value, which is explained in detail further down the page.

4. api_paste_private - this makes a paste public, unlisted or private, public = 0, unlisted = 1, private = 2

5. api_paste_expire_date - this sets the expiration date of your paste, the values are explained futher down the page.

6. api_folder_key - this sets the key of the folder of your paste, the values are explained futher down the page.

Creating A New Paste, The 'api_paste_format' Parameter In Detail

    
        We have over 200 syntax highlighting options available, below you can find a list of all the possible values you can use in combination with api_paste_format.
        Always include the value on the left from the list below, the value on the right is just the full name of the language in question.

        
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                [email](/archive/email)= Email
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
            
        
         
    

    
    
    [4cs](/archive/4cs)= 4CS

[6502acme](/archive/6502acme)= 6502 ACME Cross Asse...

[6502kickass](/archive/6502kickass)= 6502 Kick Assembler

[6502tasm](/archive/6502tasm)= 6502 TASM/64TASS

[abap](/archive/abap)= ABAP

[actionscript](/archive/actionscript)= ActionScript

[actionscript3](/archive/actionscript3)= ActionScript 3

[ada](/archive/ada)= Ada

[aimms](/archive/aimms)= AIMMS

[algol68](/archive/algol68)= ALGOL 68

[apache](/archive/apache)= Apache Log

[applescript](/archive/applescript)= AppleScript

[apt_sources](/archive/apt_sources)= APT Sources

[arduino](/archive/arduino)= Arduino

[arm](/archive/arm)= ARM

[asm](/archive/asm)= ASM (NASM)

[asp](/archive/asp)= ASP

[asymptote](/archive/asymptote)= Asymptote

[autoconf](/archive/autoconf)= autoconf

[autohotkey](/archive/autohotkey)= Autohotkey

[autoit](/archive/autoit)= AutoIt

[avisynth](/archive/avisynth)= Avisynth

[awk](/archive/awk)= Awk

[bascomavr](/archive/bascomavr)= BASCOM AVR

[bash](/archive/bash)= Bash

[basic4gl](/archive/basic4gl)= Basic4GL

[dos](/archive/dos)= Batch

[bibtex](/archive/bibtex)= BibTeX

[b3d](/archive/b3d)= Blitz3D

[blitzbasic](/archive/blitzbasic)= Blitz Basic

[bmx](/archive/bmx)= BlitzMax

[bnf](/archive/bnf)= BNF

[boo](/archive/boo)= BOO

[bf](/archive/bf)= BrainFuck

[c](/archive/c)= C

[csharp](/archive/csharp)= C#

[c_winapi](/archive/c_winapi)= C (WinAPI)

[cpp](/archive/cpp)= C++

[cpp-winapi](/archive/cpp-winapi)= C++ (WinAPI)

[cpp-qt](/archive/cpp-qt)= C++ (with Qt extensi...

[c_loadrunner](/archive/c_loadrunner)= C: Loadrunner

[caddcl](/archive/caddcl)= CAD DCL

[cadlisp](/archive/cadlisp)= CAD Lisp

[ceylon](/archive/ceylon)= Ceylon

[cfdg](/archive/cfdg)= CFDG

[c_mac](/archive/c_mac)= C for Macs

[chaiscript](/archive/chaiscript)= ChaiScript

[chapel](/archive/chapel)= Chapel

[cil](/archive/cil)= C Intermediate Langu...

[clojure](/archive/clojure)= Clojure

[klonec](/archive/klonec)= Clone C

[klonecpp](/archive/klonecpp)= Clone C++

[cmake](/archive/cmake)= CMake

[cobol](/archive/cobol)= COBOL

[coffeescript](/archive/coffeescript)= CoffeeScript

[cfm](/archive/cfm)= ColdFusion

[css](/archive/css)= CSS

[cuesheet](/archive/cuesheet)= Cuesheet

[d](/archive/d)= D

[dart](/archive/dart)= Dart

[dcl](/archive/dcl)= DCL

[dcpu16](/archive/dcpu16)= DCPU-16

[dcs](/archive/dcs)= DCS

[delphi](/archive/delphi)= Delphi

[oxygene](/archive/oxygene)= Delphi Prism (Oxygen...

[diff](/archive/diff)= Diff

[div](/archive/div)= DIV

[dot](/archive/dot)= DOT

[e](/archive/e)= E

[ezt](/archive/ezt)= Easytrieve

[ecmascript](/archive/ecmascript)= ECMAScript

[eiffel](/archive/eiffel)= Eiffel

[epc](/archive/epc)= EPC

[erlang](/archive/erlang)= Erlang

[euphoria](/archive/euphoria)= Euphoria

[fsharp](/archive/fsharp)= F#

[falcon](/archive/falcon)= Falcon

[filemaker](/archive/filemaker)= Filemaker

[fo](/archive/fo)= FO Language

[f1](/archive/f1)= Formula One

[fortran](/archive/fortran)= Fortran

[freebasic](/archive/freebasic)= FreeBasic

[freeswitch](/archive/freeswitch)= FreeSWITCH

[gambas](/archive/gambas)= GAMBAS

[gml](/archive/gml)= Game Maker

[gdb](/archive/gdb)= GDB

[gdscript](/archive/gdscript)= GDScript

[genero](/archive/genero)= Genero

[genie](/archive/genie)= Genie

[gettext](/archive/gettext)= GetText

[go](/archive/go)= Go

[godot-glsl](/archive/godot-glsl)= Godot GLSL

[groovy](/archive/groovy)= Groovy

[gwbasic](/archive/gwbasic)= GwBasic

[haskell](/archive/haskell)= Haskell

[haxe](/archive/haxe)= Haxe

[hicest](/archive/hicest)= HicEst

[hq9plus](/archive/hq9plus)= HQ9 Plus

[html4strict](/archive/html4strict)= HTML

[html5](/archive/html5)= HTML 5

[icon](/archive/icon)= Icon

[idl](/archive/idl)= IDL

[ini](/archive/ini)= INI file

[inno](/archive/inno)= Inno Script

[intercal](/archive/intercal)= INTERCAL

[io](/archive/io)= IO

[ispfpanel](/archive/ispfpanel)= ISPF Panel Definitio...

[j](/archive/j)= J

[java](/archive/java)= Java

[java5](/archive/java5)= Java 5

[javascript](/archive/javascript)= JavaScript

[jcl](/archive/jcl)= JCL

[jquery](/archive/jquery)= jQuery

[json](/archive/json)= JSON

[julia](/archive/julia)= Julia

[kixtart](/archive/kixtart)= KiXtart

[kotlin](/archive/kotlin)= Kotlin

[ksp](/archive/ksp)= KSP (Kontakt Script)

[latex](/archive/latex)= Latex

[ldif](/archive/ldif)= LDIF

[lb](/archive/lb)= Liberty BASIC

[lsl2](/archive/lsl2)= Linden Scripting

[lisp](/archive/lisp)= Lisp

[llvm](/archive/llvm)= LLVM

[locobasic](/archive/locobasic)= Loco Basic

[logtalk](/archive/logtalk)= Logtalk

[lolcode](/archive/lolcode)= LOL Code

[lotusformulas](/archive/lotusformulas)= Lotus Formulas

[lotusscript](/archive/lotusscript)= Lotus Script

[lscript](/archive/lscript)= LScript

[lua](/archive/lua)= Lua

[m68k](/archive/m68k)= M68000 Assembler

[magiksf](/archive/magiksf)= MagikSF

[make](/archive/make)= Make

[mapbasic](/archive/mapbasic)= MapBasic

[markdown](/archive/markdown)= Markdown

[matlab](/archive/matlab)= MatLab

[mercury](/archive/mercury)= Mercury

[metapost](/archive/metapost)= MetaPost

[mirc](/archive/mirc)= mIRC

[mmix](/archive/mmix)= MIX Assembler

[mk-61](/archive/mk-61)= MK-61/52

[modula2](/archive/modula2)= Modula 2

[modula3](/archive/modula3)= Modula 3

[68000devpac](/archive/68000devpac)= Motorola 68000 HiSof...

[mpasm](/archive/mpasm)= MPASM

[mxml](/archive/mxml)= MXML

[mysql](/archive/mysql)= MySQL

[nagios](/archive/nagios)= Nagios

[netrexx](/archive/netrexx)= NetRexx

[newlisp](/archive/newlisp)= newLISP

[nginx](/archive/nginx)= Nginx

[nim](/archive/nim)= Nim

[nsis](/archive/nsis)= NullSoft Installer

[oberon2](/archive/oberon2)= Oberon 2

[objeck](/archive/objeck)= Objeck Programming L...

[objc](/archive/objc)= Objective C

[ocaml](/archive/ocaml)= OCaml

[ocaml-brief](/archive/ocaml-brief)= OCaml Brief

[octave](/archive/octave)= Octave

[pf](/archive/pf)= OpenBSD PACKET FILTE...

[glsl](/archive/glsl)= OpenGL Shading

[oorexx](/archive/oorexx)= Open Object Rexx

[oobas](/archive/oobas)= Openoffice BASIC

[oracle8](/archive/oracle8)= Oracle 8

[oracle11](/archive/oracle11)= Oracle 11

[oz](/archive/oz)= Oz

[parasail](/archive/parasail)= ParaSail

[parigp](/archive/parigp)= PARI/GP

[pascal](/archive/pascal)= Pascal

[pawn](/archive/pawn)= Pawn

[pcre](/archive/pcre)= PCRE

[per](/archive/per)= Per

[perl](/archive/perl)= Perl

[perl6](/archive/perl6)= Perl 6

[phix](/archive/phix)= Phix

[php](/archive/php)= PHP

[php-brief](/archive/php-brief)= PHP Brief

[pic16](/archive/pic16)= Pic 16

[pike](/archive/pike)= Pike

[pixelbender](/archive/pixelbender)= Pixel Bender

[pli](/archive/pli)= PL/I

[plsql](/archive/plsql)= PL/SQL

[postgresql](/archive/postgresql)= PostgreSQL

[postscript](/archive/postscript)= PostScript

[povray](/archive/povray)= POV-Ray

[powerbuilder](/archive/powerbuilder)= PowerBuilder

[powershell](/archive/powershell)= PowerShell

[proftpd](/archive/proftpd)= ProFTPd

[progress](/archive/progress)= Progress

[prolog](/archive/prolog)= Prolog

[properties](/archive/properties)= Properties

[providex](/archive/providex)= ProvideX

[puppet](/archive/puppet)= Puppet

[purebasic](/archive/purebasic)= PureBasic

[pycon](/archive/pycon)= PyCon

[python](/archive/python)= Python

[pys60](/archive/pys60)= Python for S60

[q](/archive/q)= q/kdb+

[qbasic](/archive/qbasic)= QBasic

[qml](/archive/qml)= QML

[rsplus](/archive/rsplus)= R

[racket](/archive/racket)= Racket

[rails](/archive/rails)= Rails

[rbs](/archive/rbs)= RBScript

[rebol](/archive/rebol)= REBOL

[reg](/archive/reg)= REG

[rexx](/archive/rexx)= Rexx

[robots](/archive/robots)= Robots

[roff](/archive/roff)= Roff Manpage

[rpmspec](/archive/rpmspec)= RPM Spec

[ruby](/archive/ruby)= Ruby

[gnuplot](/archive/gnuplot)= Ruby Gnuplot

[rust](/archive/rust)= Rust

[sas](/archive/sas)= SAS

[scala](/archive/scala)= Scala

[scheme](/archive/scheme)= Scheme

[scilab](/archive/scilab)= Scilab

[scl](/archive/scl)= SCL

[sdlbasic](/archive/sdlbasic)= SdlBasic

[smalltalk](/archive/smalltalk)= Smalltalk

[smarty](/archive/smarty)= Smarty

[spark](/archive/spark)= SPARK

[sparql](/archive/sparql)= SPARQL

[sqf](/archive/sqf)= SQF

[sql](/archive/sql)= SQL

[sshconfig](/archive/sshconfig)= SSH Config

[standardml](/archive/standardml)= StandardML

[stonescript](/archive/stonescript)= StoneScript

[sclang](/archive/sclang)= SuperCollider

[swift](/archive/swift)= Swift

[systemverilog](/archive/systemverilog)= SystemVerilog

[tsql](/archive/tsql)= T-SQL

[tcl](/archive/tcl)= TCL

[teraterm](/archive/teraterm)= Tera Term

[texgraph](/archive/texgraph)= TeXgraph

[thinbasic](/archive/thinbasic)= thinBasic

[typescript](/archive/typescript)= TypeScript

[typoscript](/archive/typoscript)= TypoScript

[unicon](/archive/unicon)= Unicon

[uscript](/archive/uscript)= UnrealScript

[upc](/archive/upc)= UPC

[urbi](/archive/urbi)= Urbi

[vala](/archive/vala)= Vala

[vbnet](/archive/vbnet)= VB.NET

[vbscript](/archive/vbscript)= VBScript

[vedit](/archive/vedit)= Vedit

[verilog](/archive/verilog)= VeriLog

[vhdl](/archive/vhdl)= VHDL

[vim](/archive/vim)= VIM

[vb](/archive/vb)= VisualBasic

[visualfoxpro](/archive/visualfoxpro)= VisualFoxPro

[visualprolog](/archive/visualprolog)= Visual Pro Log

[whitespace](/archive/whitespace)= WhiteSpace

[whois](/archive/whois)= WHOIS

[winbatch](/archive/winbatch)= Winbatch

[xbasic](/archive/xbasic)= XBasic

[xml](/archive/xml)= XML

[xojo](/archive/xojo)= Xojo

[xorg_conf](/archive/xorg_conf)= Xorg Config

[xpp](/archive/xpp)= XPP

[yaml](/archive/yaml)= YAML

[yara](/archive/yara)= YARA

[z80](/archive/z80)= Z80 Assembler

[zxbasic](/archive/zxbasic)= ZXBasic

Creating A New Paste, The 'api_paste_expire_date' Parameter In Detail

    
        We have 9 valid values available which you can use with the api_paste_expire_date parameter:

N = Never

10M = 10 Minutes

1H = 1 Hour

1D = 1 Day

1W = 1 Week

2W = 2 Weeks

1M = 1 Month

6M = 6 Months

1Y = 1 Year

    
    
    N = Never

10M = 10 Minutes

1H = 1 Hour

1D = 1 Day

1W = 1 Week

2W = 2 Weeks

1M = 1 Month

6M = 6 Months

1Y = 1 Year

Creating A New Paste, The 'api_paste_private' Parameter In Detail

    
        We have 3 valid values available which you can use with the api_paste_private parameter:

0 = Public

1 = Unlisted

2 = Private (only allowed in combination with api_user_key, as you have to be logged into your account to access the paste)

    
    
    0 = Public

1 = Unlisted

2 = Private (only allowed in combination with api_user_key, as you have to be logged into your account to access the paste)

Creating A New Paste, The 'api_folder_key' Parameter In Detail

    
        With this parameter you can set the destination folder for your paste. Use the 'api_user_key' parameter first before using 'api_folder_key' of your existing folder.
    

    
    
    Creating An 'api_user_key' Using The API Member Login System

    
        With this API we allow you to create applications which use the Pastebin members system.
        Sending a valid POST request to our API login system will return a unique api_user_key which can then be used to create a paste as a logged in user.
        Please send the request to the link shown below:
        

1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_name - this is the username of the user you want to login.

3. api_user_password - this is the password of the user you want to login.

If all 3 values match, a valid user session key will be returned. This key can be used as the api_user_key parameter. Only one key can be active at the same time for the same user. This key does not expire, unless a new one is generated. We recommend creating just one, then caching that key locally as it does not expire.

Below is a PHP example using curl how to create a valid api_user_key:

    
    
    https://pastebin.com/api/api_login.php

        Include all the following POST parameters when you request the url:
1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_name - this is the username of the user you want to login.

3. api_user_password - this is the password of the user you want to login.

If all 3 values match, a valid user session key will be returned. This key can be used as the api_user_key parameter. Only one key can be active at the same time for the same user. This key does not expire, unless a new one is generated. We recommend creating just one, then caching that key locally as it does not expire.

Below is a PHP example using curl how to create a valid api_user_key:

$api_dev_key 		= 'YOUR API DEVELOPER KEY';
$api_user_name 		= 'a_users_username';
$api_user_password 	= 'a_users_password';
$api_user_name 		= urlencode($api_user_name);
$api_user_password 	= urlencode($api_user_password);
$url			= 'https://pastebin.com/api/api_login.php';
$ch			= curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'api_dev_key='.$api_dev_key.'&api_user_name='.$api_user_name.'&api_user_password='.$api_user_password.'');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_NOBODY, 0);
$response 		= curl_exec($ch);
echo $response;

        Below is a curl command example how to create a valid api_user_key:
        curl -X POST -d 'api_dev_key=YOUR API DEVELOPER KEY' -d 'api_user_name=a_users_username' -d 'api_user_password=a_users_password' "https://pastebin.com/api/api_login.php"

        Possible Good API Responses: (example)
        6c6d3fe13b19bbd6e479b705df0a607f

        Possible Bad API Responses:
        Bad API request, use POST request, not GET
Bad API request, invalid api_dev_key
Bad API request, invalid login
Bad API request, account not active
Bad API request, invalid POST parameters

    Listing Pastes Created By A User

    
        With this API you can list all the pastes created by a certain user. You will need send a valid POST request to the url below to access the data:
        

1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

3. api_results_limit - this is not required, by default its set to 50, min value is 1, max value is 1000

4. api_option - set as 'list'

Below is a PHP example using curl how to list pastes:

    
    
    https://pastebin.com/api/api_post.php

        Include all the following POST parameters when you request the url:
1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

[How to obtain such a key](#9)
3. api_results_limit - this is not required, by default its set to 50, min value is 1, max value is 1000

4. api_option - set as 'list'

Below is a PHP example using curl how to list pastes:

$api_dev_key 		= 'YOUR API DEVELOPER KEY';
$api_user_key 		= '';
$api_results_limit 	= '100';
$url 			= 'https://pastebin.com/api/api_post.php';
$ch 			= curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'api_option=list&api_user_key='.$api_user_key.'&api_dev_key='.$api_dev_key.'&api_results_limit='.$api_results_limit.'');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_NOBODY, 0);
$response  		= curl_exec($ch);
echo $response;

        Below is a curl command example how to list pastes:
        curl -X POST -d 'api_dev_key=YOUR API DEVELOPER KEY' -d 'api_user_key=YOUR API USER KEY' -d 'api_option=list' -d 'api_results_limit=100' "https://pastebin.com/api/api_post.php"

        Below is an example output of a users paste listing:
        <paste>
        <paste_key>0b42rwhf</paste_key>
        <paste_date>1297953260</paste_date>
        <paste_title>javascript test</paste_title>
        <paste_size>15</paste_size>
        <paste_expire_date>1297956860</paste_expire_date>
        <paste_private>0</paste_private>
        <paste_format_long>JavaScript</paste_format_long>
        <paste_format_short>javascript</paste_format_short>
        <paste_url>https://pastebin.com/0b42rwhf</paste_url>
        <paste_hits>15</paste_hits>
</paste>
<paste>
        <paste_key>0C343n0d</paste_key>
        <paste_date>1297694343</paste_date>
        <paste_title>Welcome To Pastebin V3</paste_title>
        <paste_size>490</paste_size>
        <paste_expire_date>0</paste_expire_date>
        <paste_private>0</paste_private>
        <paste_format_long>None</paste_format_long>
        <paste_format_short>text</paste_format_short>
        <paste_url>https://pastebin.com/0C343n0d</paste_url>
        <paste_hits>65</paste_hits>
</paste>

        Other Possible Good API Responses:
        No pastes found.

        Possible Bad API Responses:
        Bad API request, invalid api_option
Bad API request, invalid api_dev_key
Bad API request, invalid api_user_key

    Deleting A Paste Created By A User

    
        With this API you can delete pastes created by certain users. You will need to send a valid POST request to the url below to access the data:
        

1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

3. api_paste_key - this is the unique key of the paste you want to delete.

4. api_option - set as 'delete'

Below is a PHP example using curl how to delete a paste:

    
    
    https://pastebin.com/api/api_post.php

        Include all the following POST parameters when you request the url:
1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

[How to obtain such a key](#9)
3. api_paste_key - this is the unique key of the paste you want to delete.

4. api_option - set as 'delete'

Below is a PHP example using curl how to delete a paste:

$api_dev_key 		= 'YOUR API DEVELOPER KEY';
$api_user_key 		= '';
$api_paste_key 		= '';
$url 			= 'https://pastebin.com/api/api_post.php';
$ch 			= curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'api_option=delete&api_user_key='.$api_user_key.'&api_dev_key='.$api_dev_key.'&api_paste_key='.$api_paste_key.'');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_NOBODY, 0);
$response  		= curl_exec($ch);
echo $response;

        Below is a curl command example how to delete a paste:
        curl -X POST -d 'api_dev_key=YOUR API DEVELOPER KEY' -d 'api_user_key=YOUR API USER KEY' -d 'api_option=delete' -d 'api_paste_key=API PASTE KEY' "https://pastebin.com/api/api_post.php"

        Possible Good API Responses:
        Paste Removed

        Possible Bad API Responses:
        Bad API request, invalid api_option
Bad API request, invalid api_dev_key
Bad API request, invalid api_user_key
Bad API request, invalid permission to remove paste

    Getting A Users Information And Settings

    
        With this API you can obtain a users personal information and certain settings. You will need to send a valid POST request to the url below to access the data:
        

1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

3. api_option - set as 'userdetails'

Below is a PHP example using curl how to get user information:

    
    https://pastebin.com/api/api_post.php

        Include all the following POST parameters when you request the url:
1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

[How to obtain such a key](#9)
3. api_option - set as 'userdetails'

Below is a PHP example using curl how to get user information:

$api_dev_key 		= 'YOUR API DEVELOPER KEY';
$api_user_key 		= '';
$url 			= 'https://pastebin.com/api/api_post.php';
$ch 			= curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'api_option=userdetails&api_user_key='.$api_user_key.'&api_dev_key='.$api_dev_key.'');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_NOBODY, 0);
$response  		= curl_exec($ch);
echo $response;

        Below is a curl command example how to get user information:
        curl -X POST -d 'api_dev_key=YOUR API DEVELOPER KEY' -d 'api_user_key=YOUR API USER KEY' -d 'api_option=userdetails' "https://pastebin.com/api/api_post.php"

        Below is an example output of a user information listing:
        <user>
        <user_name>wiz_kitty</user_name>
        <user_format_short>text</user_format_short>
        <user_expiration>N</user_expiration>
        <user_avatar_url>https://pastebin.com/cache/a/1.jpg</user_avatar_url>
        <user_private>1</user_private> (0 Public, 1 Unlisted, 2 Private)
        <user_website>https://myawesomesite.com</user_website>
        <user_email>

        Possible Bad API Responses:
        [\[email protected\]](/cdn-cgi/l/email-protection)</user_email> <user_location>New York</user_location> <user_account_type>1</user_account_type> (0 normal, 1 PRO) </user>
Bad API request, invalid api_option
Bad API request, invalid api_dev_key
Bad API request, invalid api_user_key

    

Getting raw paste output of users pastes including 'private' pastes

    
        With this API you can obtain the raw paste output of a users pastes, including private pastes:
        

1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

3. api_paste_key - this is paste key you want to fetch the data from.

4. api_option - set as 'show_paste'

Below is a PHP example using curl how to fetch a users raw paste output:

    
    
    https://pastebin.com/api/api_raw.php

        Include all the following POST parameters when you request the url:
1. api_dev_key - this is your API Developer Key, in your case: YOUR API DEVELOPER KEY

2. api_user_key - this is the session key of the logged in user.

[How to obtain such a key](#9)
3. api_paste_key - this is paste key you want to fetch the data from.

4. api_option - set as 'show_paste'

Below is a PHP example using curl how to fetch a users raw paste output:

$api_dev_key 		= 'YOUR API DEVELOPER KEY';
$api_user_key 		= '';
$url 			= 'https://pastebin.com/api/api_raw.php';
$ch 			= curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, 'api_option=show_paste&api_user_key='.$api_user_key.'&api_dev_key='.$api_dev_key.'&api_paste_key=A_VALID_PASTE_KEY_HERE');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_NOBODY, 0);
$response  		= curl_exec($ch);
echo $response;

        Below is a curl command example how to fetch a users raw paste output:
        curl -X POST -d 'api_dev_key=YOUR API DEVELOPER KEY' -d 'api_user_key=YOUR API USER KEY' -d 'api_option=show_paste' -d 'api_paste_key=API PASTE KEY' "https://pastebin.com/api/api_post.php"

        Possible Bad API Responses:
        Bad API request, invalid api_option
Bad API request, invalid api_dev_key
Bad API request, invalid api_user_key
Bad API request, invalid permission to view this paste or invalid api_paste_key

    Getting raw paste output of any 'public' & 'unlisted' pastes

    This option is actually not part of our API, but you might still want to use it. To get the raw output of any public or unlisted paste you can use our raw data output url:
        
    

https://pastebin.com/raw/

        Simply add the paste_key at the end of that url and you will get the raw output.
        **TIP:**If you are trying to scrape our content, check out

[our scraping API](/doc_scraping_api).
