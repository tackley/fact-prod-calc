temporarily hard coded in the UI is: 
  Game = "Captain of Industry"
  ElectricityMultiplier = 1.0 (this derived in game from the difficulty level in CoI)


What item do you want to produce?

BACKEND CALL:
  GET http://localhost:5000/coi/items

RETURNS
  {
    items: [
      "Uranium rod",
      "Brine",
      ...
    ]
  }



BACKEND CALL:
  GET https://localhost:5000/coi/recipes?item=Brine&net_amount=50

RETURNS
  {
    recipes: [
      {
        inputs: [
          {
            item: "Seawater",
            amountPerStep: 20,
            amount: 40,
          }
        ],
        outputs: [
          {
            item: "Brine",
            amountPerStep: 1,
            amount: 2
          }
        ],
        machine: "Evaporutsativesajrthe Pond"
        stepDuration: 30
        id: "205"
      }
    ]
  }


BACKEND CALL:
  POST https://localhost:5000/coi/calc

  SUBMITTED BODY:
  {
    chosenRecipes: {
      inputs: [
        {
          item: "Brine",
          recipeId: "205"
        }
      ],
      outputs: [
        {
          item: "Brine",
          recipeId: "205"
        }
      ]
    },
    requiredItems: [
      {
        item: "Brine",
        amount: 50
      }
    ]
  }


  RETURNS
  {
    productionRates: [
      {
        item: "Brine"
        amount: 50
      }
    ]
  }