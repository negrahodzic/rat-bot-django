console.log("Script is called!");

function isElementInViewport(el) {
  const rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
    rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

window.addEventListener('scroll', function() {
//  const featureElements = document.querySelectorAll('.feature_typing');
  featureElements.forEach(function(featureElement) {
    if (isElementInViewport(featureElement)) {
        featureElement.classList.add('start_typing');
    }
  });
});

let featureElements = document.querySelectorAll('.feature_typing');
window.addEventListener('load', function() {
  featureElements = document.querySelectorAll('.feature_typing');
  featureElements.forEach(function(featureElement) {
    if (isElementInViewport(featureElement)) {
        featureElement.classList.add('start_typing');
    }
  });
});