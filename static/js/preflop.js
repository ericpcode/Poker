function updateSliderValue(value) {
    document.getElementById('slider-value').innerText = value + '%';
  }
  function clearSelectedCells() {
    // Clear the selected cells list
    selectedCells = [];
    
    // Reset the cell background colors
    var cells = document.getElementsByTagName('td');
    for (var i = 0; i < cells.length; i++) {
      cells[i].classList.remove("clicked");
    }
    
    updateSelectedCellsDisplay(selectedCells);
  }

  var isMouseDown = false;
  var selectedCells = [];

  function toggleCell(cell) {
    var cellValue = cell.innerText;

    if (selectedCells.includes(cellValue)) {
      // Deselect the cell
      cell.classList.remove("clicked");
      selectedCells = selectedCells.filter(value => value !== cellValue);
    } else {        
      // Select the cell
      cell.classList.add("clicked");
      selectedCells.push(cellValue);
      console.log(cell.getAttribute("id"));
    }

    sortSelectedCells();
  }

  function sortSelectedCells() {
    var data = JSON.stringify({
        selected_cells: selectedCells
    });

      fetch('/sort-cells', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: data
      })
      .then(response => response.json())
      .then(data => {
          var sortedCells = data.sorted_cells;
          updateSelectedCellsDisplay(sortedCells);
      })
      .catch(error => {
          console.error('Request failed:', error);
      });
  }


  function updateSelectedCellsDisplay(sortedCells) {
    var selectedCellsElement = document.getElementById('selected-cells');
    selectedCellsElement.innerHTML = '<strong>Selected Hands:</strong> ' + sortedCells.join(', ');
  }

  document.addEventListener('mousedown', function() {
    isMouseDown = true;
  });

  document.addEventListener('mouseup', function() {
    isMouseDown = false;
    updateSelectedCellsDisplay();
  });

  document.querySelectorAll('td').forEach(function(cell) {
    cell.addEventListener('mouseover', function() {
      if (isMouseDown) {
        toggleCell(cell);
      }
    });
  });

  function updateSelectedTopRangeCellsDisplay(sortedCells){
    var selectedCellsElement = document.getElementById('selected-cells');
    selectedCellsElement.innerHTML = '<strong>Selected Hands:</strong> ' + sortedCells.join(', ');

    // Reset the cell background colors
    var cells = document.getElementsByTagName('td');
    for (var i = 0; i < cells.length; i++) {
      cells[i].classList.remove("clicked");
    }
    // Need to ungroup sortedCells with a python function call, remove the slicing ind cellId

    fetch('/ungroup-hands', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        selected_cells: sortedCells
      })
    })
    .then(response => response.json())
    .then(data => {
      var ungroupedCells = data.sorted_cells;

      // Add highlighting to the table cells corresponding to selected hands
      ungroupedCells.forEach(function(cellId) {
        var cell = document.getElementById(cellId);
        if (cell) {
          cell.classList.add('clicked');
        }
      });
    })
    .catch(error => {
      console.error('Request failed:', error);
    });
  }

  function calculateTopRange() {
    var percentageSlider = document.getElementById('percentage-slider');
    var percentage = percentageSlider.value;

    // Make an AJAX request to the server
    $.ajax({
      type: "POST",
      url: "/calculate-top-range",
      data: JSON.stringify({ percentage: percentage }),
      contentType: "application/json",
      success: function(response) {
        // Update the selected hands list with the calculated result
        var calculatedHands = response.calculated_hands;
        selectedHands = calculatedHands;
        updateSelectedTopRangeCellsDisplay(selectedHands);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }

  document.getElementById('calculate-button').addEventListener('click', function() {
    console.log('Button clicked!');
    calculateTopRange();
  });

  // Call the function to update the initial display
  updateSelectedCellsDisplay();