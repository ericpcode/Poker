from flask import Flask, render_template, request, jsonify
from preflop_range_calculator import generate_two_card_hands, group_hands, calculate_top_range_str, ungroup_hands
from deck_of_cards import Deck, convert_card_list_str

app = Flask(__name__)

# Define the route for the index page
@app.route('/')
def index():
    two_card_hands = generate_two_card_hands()
    return render_template('index.html', hands= two_card_hands)

# Define the route for the calculator page
@app.route('/calculate')
def calculate():
    deck = Deck()
    cards = convert_card_list_str(deck.cards)
    return render_template('calculator.html', cards = cards)


@app.route('/sort-cells', methods=['POST'])
def sort_cells():
  data = request.get_json()
  selected_cells = data.get("selected_cells", [])

  # Call the group_hands function to sort the selected cells
  sorted_cells = group_hands(selected_cells)

  # Return the sorted result as JSON
  return jsonify({"sorted_cells": sorted_cells})

@app.route('/calculate-top-range', methods=['POST'])
def calculate_top_range():
    data = request.get_json()
    percentage = data.get("percentage", 0)

    # Call the calculate_top_range_str function to calculate the top range
    calculated_hands = group_hands(calculate_top_range_str(int(percentage)))

    # Return the calculated result as JSON
    return jsonify({"calculated_hands": calculated_hands})

@app.route('/ungroup-hands', methods=['POST'])
def ungroup_sort_hands():
  data = request.get_json()
  selected_cells = data.get("selected_cells", [])

  # Call the group_hands function to sort the selected cells
  ungrouped_cells = ungroup_hands(selected_cells)

  # Return the sorted result as JSON
  return jsonify({"sorted_cells": ungrouped_cells})

if __name__ == '__main__':
    app.run()