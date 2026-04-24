---
id: 2856
date: 2025-10-10T20:20:19+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

``⎕CR 'PrimeNumbers'  ⍝ Show APL user-function PrimeNumbers
Primes←PrimeNumbers N     ⍝ Function takes one right arg N (e.g., show prime numbers for 1 ... int N)
Primes←(2=+⌿0=(⍳N)∘.|⍳N)/⍳N  ⍝ The Ken Iverson one-liner
      PrimeNumbers 100    ⍝ Show all prime numbers from 1 to 100
2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97
      ⍴PrimeNumbers 100
25                       ⍝ There are twenty-five prime numbers in the range up to 100`.`

Ух, бля. Ну короче APL из тех языков, для которых надо читать мануал чтобы понять что написано.

С комбинаторными языками вообще так. Если вы с ними не сталкивались, вы вряд ли сходу поймёте даже с объяснениями.