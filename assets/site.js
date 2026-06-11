(function () {
	function ready(callback) {
		if (document.readyState === "loading") {
			document.addEventListener("DOMContentLoaded", callback);
			return;
		}
		callback();
	}

	ready(function () {
		var sidebarToggle = document.getElementById("strixieSidebarToggle");
		var mobileOpen = document.querySelector("[data-mobile-nav-open]");
		var mobileClose = document.querySelector("[data-mobile-nav-close]");
		var backdrop = document.querySelector("[data-nav-backdrop]");
		var filterInput = document.querySelector("[data-filter-input]");

		function setCollapsed(collapsed) {
			document.documentElement.classList.toggle("strixie-sidebar-collapsed", collapsed);
			if (sidebarToggle) {
				sidebarToggle.setAttribute("aria-pressed", collapsed ? "true" : "false");
				sidebarToggle.setAttribute("aria-label", collapsed ? "Expand navigation" : "Collapse navigation");
				sidebarToggle.textContent = collapsed ? ">" : "<";
			}
		}

		try {
			setCollapsed(window.sessionStorage.getItem("hardiman.sidebar.collapsed") === "true");
		} catch (error) {
			setCollapsed(false);
		}

		if (sidebarToggle) {
			sidebarToggle.addEventListener("click", function () {
				var collapsed = !document.documentElement.classList.contains("strixie-sidebar-collapsed");
				setCollapsed(collapsed);
				try {
					window.sessionStorage.setItem("hardiman.sidebar.collapsed", collapsed ? "true" : "false");
				} catch (error) {
					// Storage is optional.
				}
			});
		}

		function setMobileNav(open) {
			document.body.classList.toggle("nav-open", open);
		}

		if (mobileOpen) {
			mobileOpen.addEventListener("click", function () {
				setMobileNav(true);
			});
		}

		if (mobileClose) {
			mobileClose.addEventListener("click", function () {
				setMobileNav(false);
			});
		}

		if (backdrop) {
			backdrop.addEventListener("click", function () {
				setMobileNav(false);
			});
		}

		document.addEventListener("keydown", function (event) {
			if (event.key === "Escape") {
				setMobileNav(false);
			}
		});

		if (filterInput) {
			filterInput.addEventListener("input", function () {
				var query = filterInput.value.trim().toLowerCase();
				document.querySelectorAll("[data-filter-item]").forEach(function (item) {
					var haystack = (item.getAttribute("data-filter-item") || "").toLowerCase();
					item.hidden = query.length > 0 && haystack.indexOf(query) === -1;
				});
			});
		}
	});
})();
