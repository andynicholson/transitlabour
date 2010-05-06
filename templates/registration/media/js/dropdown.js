
var timeout    = 500;
var closetimer = 0;
var ddmenuitem = 0;

function jsddm_open()
{  jsddm_canceltimer();
   jsddm_close();
   ddmenuitem = $(this).find('ul').css('visibility', 'visible');}

function jsddm_close()
{  if(ddmenuitem) ddmenuitem.css('visibility', 'hidden');}

function jsddm_timer()
{  closetimer = window.setTimeout(jsddm_close, timeout);}

function jsddm_canceltimer()
{  if(closetimer)
   {  window.clearTimeout(closetimer);
      closetimer = null;}}

$(document).ready(function()
{  $('#jsddm > li').bind('mouseover', jsddm_open)
   $('#jsddm > li').bind('mouseout',  jsddm_timer)
 });

document.onclick = jsddm_close;



function jscdm_open()
{  jscdm_canceltimer();
   jscdm_close();
   ddmenuitem = $(this).find('ul').css('visibility', 'visible');}

function jscdm_close()
{  if(ddmenuitem) ddmenuitem.css('visibility', 'hidden');}

function jscdm_timer()
{  closetimer = window.setTimeout(jscdm_close, timeout);}

function jscdm_canceltimer()
{  if(closetimer)
   {  window.clearTimeout(closetimer);
      closetimer = null;}}

$(document).ready(function()
{  $('#jscdm > li').bind('mouseover', jscdm_open)
   $('#jscdm > li').bind('mouseout',  jscdm_timer)
 });

document.onclick = jscdm_close;

