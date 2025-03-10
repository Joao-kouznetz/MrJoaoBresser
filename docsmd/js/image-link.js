document.addEventListener("DOMContentLoaded", function () {
	// Find all links that contain images directly as children
	const imageLinks = document.querySelectorAll("a > img");

	imageLinks.forEach((img) => {
		const link = img.parentNode;
		// Create wrapper div
		const wrapper = document.createElement("div");
		wrapper.className = "clickable-image-container";

		// Insert wrapper before the link in the DOM
		link.parentNode.insertBefore(wrapper, link);

		// Move link inside wrapper
		wrapper.appendChild(link);
	});
});
