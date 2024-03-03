Scenario recipes:
Assembly (electric) performing 6 Iron --> 4 Mechanical parts in 30s.
Metal caster performing 12 Molten iron --> 12 Iron in 30s.
Blast furnace performing 8 Iron ore + 2 Coal --> 8 Molten iron + 4 Exhaust in 20s.


1. Front end calls `GET /coi/items`
 returns Iron, Mechanical parts, Molten iron, Iron ore, Coal, Exhaust

 2. User selects "Mechanical parts" at 1 / min
BACKEND CALL:
  POST https://localhost:5000/coi/calc

  SUBMITTED BODY:
  {
    chosenRecipes: {
      producing: [],
      consuming: []
    },
    requiredItems: [
      {
        item: "Mechanical parts",
        amount: 1
      }
    ]
  }
  RETURNS:
  {
    productionRates: []
    requiredInputs: [
      {
        item: "Mechanical parts"
        amount: 1
      }
    ]
  }

ui needs to draw:

output - mech parts 1/min.
input - mech parts 1/min

3. user clicks input node
front end calls `GET /coi/recipes?item=Mechanical%20parts&net_amount=1`
finds 1 recipe (Assembly (electric) performing 6 Iron --> 4 Mechanical parts in 30s.) and displays it

 {
        inputs: [
          {
            item: "Iron",
            amountPerStep: 6,
            amount: 12,
          }
        ],
        outputs: [
          {
            item: "Mechanical Parts",
            amountPerStep: 4,
            amount: 8
          }
        ],
        machine: "Assembly (electric)"
        stepDuration: 30
        id: "205"
      }

user clicks on recipe

4. graph is updated
BACKEND CALL:
  POST https://localhost:5000/coi/calc

  SUBMITTED BODY:
  {
    chosenRecipes: {
      producing: [
        {
          item: "Mechanical parts",
          recipeId: "0"
        }
      ],
      consuming: []
    },
    requiredItems: [
      {
        item: "Mechanical parts",
        amount: 1
      }
    ]
  }
  RETURNS:
  {
    productionRates: [
      {
        item: "Mechanical parts"
        amount: 1
      }
    ]
    requiredInputs: [
      {
        item: "Iron"
        amount: 1.5
      }
    ]
    recipes: [
      {
        recipe:  {
          inputs: [
            {
              item: "Iron",
              amountPerStep: 6,
              amount: 12,
            }
          ],
          outputs: [
            {
              item: "Mechanical Parts",
              amountPerStep: 4,
              amount: 8
            }
          ],
          machine: "Assembly (electric)"
          stepDuration: 30
          id: "205"
        },
        instances: 0.125
      }
    ]
  }
