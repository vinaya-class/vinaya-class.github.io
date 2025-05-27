// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded affix "><a href="vinaya-class.html">Vinaya Class</a></li><li class="chapter-item expanded affix "><a href="pali-sutta-readings.html">Pāli Sutta Readings</a></li><li class="chapter-item expanded affix "><a href="pali-lessons.html">Pāli Lessons</a></li><li class="chapter-item expanded affix "><a href="00-introduction.html">Introduction</a></li><li class="chapter-item expanded "><a href="01-killing-and-harming.html"><strong aria-hidden="true">1.</strong> Killing and Harming</a></li><li class="chapter-item expanded "><a href="02-stealing.html"><strong aria-hidden="true">2.</strong> Stealing</a></li><li class="chapter-item expanded "><a href="03-sexual-conduct.html"><strong aria-hidden="true">3.</strong> Sexual Conduct</a></li><li class="chapter-item expanded "><a href="04-lustful-conduct.html"><strong aria-hidden="true">4.</strong> Lustful Conduct</a></li><li class="chapter-item expanded "><a href="05-women-1.html"><strong aria-hidden="true">5.</strong> Women 1</a></li><li class="chapter-item expanded "><a href="06-attainments.html"><strong aria-hidden="true">6.</strong> Attainments</a></li><li class="chapter-item expanded "><a href="07-false-speech.html"><strong aria-hidden="true">7.</strong> False Speech</a></li><li class="chapter-item expanded "><a href="08-robes-1.html"><strong aria-hidden="true">8.</strong> Robes 1</a></li><li class="chapter-item expanded "><a href="09-kiccavatta.html"><strong aria-hidden="true">9.</strong> Kiccavatta</a></li><li class="chapter-item expanded "><a href="10-misc-1.html"><strong aria-hidden="true">10.</strong> Misc 1</a></li><li class="chapter-item expanded "><a href="11-food-1.html"><strong aria-hidden="true">11.</strong> Food 1</a></li><li class="chapter-item expanded "><a href="12-food-2.html"><strong aria-hidden="true">12.</strong> Food 2</a></li><li class="chapter-item expanded "><a href="13-money.html"><strong aria-hidden="true">13.</strong> Money</a></li><li class="chapter-item expanded "><a href="14-arguments-1.html"><strong aria-hidden="true">14.</strong> Arguments 1</a></li><li class="chapter-item expanded "><a href="15-arguments-2.html"><strong aria-hidden="true">15.</strong> Arguments 2</a></li><li class="chapter-item expanded "><a href="16-arguments-3.html"><strong aria-hidden="true">16.</strong> Arguments 3</a></li><li class="chapter-item expanded "><a href="17-dwellings.html"><strong aria-hidden="true">17.</strong> Dwellings</a></li><li class="chapter-item expanded "><a href="18-bowls.html"><strong aria-hidden="true">18.</strong> Bowls</a></li><li class="chapter-item expanded "><a href="19-women-2.html"><strong aria-hidden="true">19.</strong> Women 2</a></li><li class="chapter-item expanded "><a href="20-misc-2.html"><strong aria-hidden="true">20.</strong> Misc 2</a></li><li class="chapter-item expanded "><a href="21-sekhiyas-1.html"><strong aria-hidden="true">21.</strong> Sekhiyas 1</a></li><li class="chapter-item expanded "><a href="22-excuses.html"><strong aria-hidden="true">22.</strong> Excuses</a></li><li class="chapter-item expanded "><a href="23-sekhiyas-2.html"><strong aria-hidden="true">23.</strong> Sekhiyas 2</a></li><li class="chapter-item expanded "><a href="24-robes-2.html"><strong aria-hidden="true">24.</strong> Robes 2</a></li><li class="chapter-item expanded "><a href="25-misc-3.html"><strong aria-hidden="true">25.</strong> Misc 3</a></li><li class="chapter-item expanded affix "><a href="99-closing.html">Closing</a></li><li class="chapter-item expanded affix "><a href="99-further-reading.html">Further Reading</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
