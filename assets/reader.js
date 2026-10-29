(function(){
"use strict";
function setup(){
if(document.body.classList.contains("reader-enabled"))return;
var body=document.body;
var top=document.createElement("div");top.className="reader-top";
top.innerHTML='<a class="reader-brand" href="../index.html">Robotics Knowledge Lab</a><div class="reader-actions"><button type="button" class="reader-btn" id="reader-back">← 뒤로가기</button><a class="reader-btn" href="../index.html" style="text-decoration:none">목록</a></div>';
var progress=document.createElement("div");progress.className="reader-progress";progress.setAttribute("role","progressbar");progress.setAttribute("aria-label","문서 읽기 진행률");progress.setAttribute("aria-valuemin","0");progress.setAttribute("aria-valuemax","100");
var layout=document.createElement("div");layout.className="reader-layout";var main=document.createElement("main");main.className="reader-main";main.id="reader-content";
while(body.firstChild){main.appendChild(body.firstChild)}
var aside=document.createElement("aside");aside.className="reader-toc";aside.setAttribute("aria-label","이 문서의 목차");var m=document.createElement("details");m.className="reader-mobile-toc";m.innerHTML="<summary>☰ 문서 목차 열기</summary>";
layout.appendChild(main);layout.appendChild(aside);main.insertBefore(m,main.firstChild);
var floating=document.createElement("div");floating.className="reader-floating";floating.innerHTML='<button type="button" class="reader-btn" id="reader-top" title="맨 위로 이동">↑ 맨 위로</button>';
body.appendChild(top);body.appendChild(progress);body.appendChild(layout);body.appendChild(floating);body.classList.add("reader-enabled");
document.getElementById("reader-back").addEventListener("click",function(){if(history.length>1&&document.referrer&&new URL(document.referrer).origin===location.origin){history.back()}else{location.href="../index.html"}});
document.getElementById("reader-top").addEventListener("click",function(){window.scrollTo({top:0,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"instant":"smooth"})});
var headings=Array.from(main.querySelectorAll("h2,h3")).filter(function(el){return el.textContent.trim().length>0});var used=new Set();
headings.forEach(function(el,i){var id=el.id||"section-"+(i+1);while(used.has(id)||document.getElementById(id)&&document.getElementById(id)!==el)id+="-x";el.id=id;used.add(id)});
function tocItems(){return headings.map(function(h){var a=document.createElement("a");a.href="#"+h.id;a.textContent=h.textContent.trim().slice(0,110);a.dataset.level=h.tagName.slice(1);a.addEventListener("click",function(){m.open=false});return a})}
aside.innerHTML='<div class="reader-toc-label">이 문서의 목차</div>';tocItems().forEach(function(a){aside.appendChild(a)});tocItems().forEach(function(a){m.appendChild(a)});
function update(){var d=document.documentElement;var total=d.scrollHeight-innerHeight;var value=total>0?Math.min(100,Math.max(0,Math.round(scrollY/total*100))):100;progress.style.width=value+"%";progress.setAttribute("aria-valuenow",String(value));var current=null;headings.forEach(function(h){if(h.getBoundingClientRect().top<=145)current=h.id});aside.querySelectorAll("a").forEach(function(a){a.classList.toggle("active",a.getAttribute("href")==="#"+current)})}
addEventListener("scroll",update,{passive:true});addEventListener("resize",update);update()
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",setup);else setup()
})();