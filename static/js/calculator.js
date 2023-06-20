var deckCells = document.getElementsByClassName('clicked-deck');
var boardPlayerCells = document.getElementsByClassName('group-clicks');

function removeClickedClass(elements) {
  for (var i = 0; i < elements.length; i++) {
    elements[i].classList.remove('clicked');
  }
}

function toggleClickedClass(element) {
  element.classList.toggle('clicked');
}

for (var i = 0; i < deckCells.length; i++) {
  deckCells[i].addEventListener('click', function() {
    if (this.classList.contains('clicked')) {
      this.classList.remove('clicked');
    } else {
      removeClickedClass(deckCells);
      this.classList.add('clicked');
    }
  });
}

for (var i = 0; i < boardPlayerCells.length; i++) {
  boardPlayerCells[i].addEventListener('click', function() {
    if (this.classList.contains('clicked')) {
      this.classList.remove('clicked');
    } else {
      removeClickedClass(boardPlayerCells);
      this.classList.add('clicked');
    }
  });
}