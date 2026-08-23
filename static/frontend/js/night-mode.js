// Night Mode JS
(function (window, document, undefined) {
	'use strict';
	if (!('localStorage' in window)) return;
	var nightMode = localStorage.getItem('gmtNightMode');
	if (nightMode) {
		document.documentElement.className += ' night-mode';
	}
})(window, document);

(function (window, document, undefined) {
	'use strict';
	if (!('localStorage' in window)) return;

	function updateNightModeUI() {
		var isNight = document.documentElement.classList.contains('night-mode');
		var themeIcons = document.querySelectorAll('.theme-icon, .btn-night-mode i');
		var themeTexts = document.querySelectorAll('.theme-text');

		themeIcons.forEach(function (icon) {
			if (isNight) {
				icon.classList.remove('uil-moon');
				icon.classList.add('uil-sun');
			} else {
				icon.classList.remove('uil-sun');
				icon.classList.add('uil-moon');
			}
		});

		themeTexts.forEach(function (text) {
			text.textContent = isNight ? 'Light Mode' : 'Dark Mode';
		});
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', updateNightModeUI);
	} else {
		updateNightModeUI();
	}

	document.addEventListener('click', function (event) {
		var btn = event.target.closest('#night-mode, .btn-night-mode');
		if (!btn) return;

		event.preventDefault();
		document.documentElement.classList.toggle('night-mode');
		if (document.documentElement.classList.contains('night-mode')) {
			localStorage.setItem('gmtNightMode', true);
		} else {
			localStorage.removeItem('gmtNightMode');
		}
		updateNightModeUI();
	}, false);

})(window, document);