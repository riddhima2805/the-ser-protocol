### Main algorithm

the main algorithm used here is BFS(breadth first search). In bfs we dont follow one path it explores all path equally layer by layer. it gives us the shortest possible path needed to reach the target. because it checks the nearby places first. for example it first checks all the places that are 1 step away then the places that are 2 step away and so on.

## Main strategy

it checks if it has a clear shot at the enemy if yes and it has AMMO, it shoots immediately. If AMMO is empty, it moves toward the nearest AMMO pack. and again with the help of bfs it finds shortest possible path to AMMO pack.

the bot detects AMMO is 0 and immediately switches goal instead of chasing the enemy, it aims towards the AMMO pack. It takes the shortest route, with the help of bfs picks up the pack and gains 5 AMMO
We should give picking an AMMO priority over other moves because a bot with no AMMO that keeps chasing the enemy is just a moving target. it wont be able to win the game without shooting the other tank for which it needs AMMO.

the bot checks if the enemy shares the same row or column and verifies no WALL sits between them. if it finds the path is clear and AMMO is available, it fires instantly.
It shoots the moment a clear shot exists, dealing 25 damage before the enemy can react.

the bot never goes after health packs. It only chases AMMO or the enemy. So if my bot is at 25 hp and a health pack is right next to it but the enemy is in same row or column with no obstacles the bot will shoot first instead of healing first.

the bot has no logic to recognize when healing is more important than attacking, which is a tieback of this code.

also earlier the main working logic of both the bots was same so the match was always ending in a tie.i tried changing a few things like adding walls in the line where they were meeting and shooting each other but even after that the match was ending in a tie so i realized the real issue was grid itself because it is desgined to be symmetric both bots end up in same line . Also since both bots are same if one is able to shoot other then other also realizes that theres no obstacle between them and he can also shoot. so both of them end up shooting simultaneously leaving the match in a tie always. so i changed the bots and one of them if it sees the enemy in line of sight then it first tries to dodge and survive rather than attacking. while the aggressive bot is a little immature. even if it sees the enemy in line of sight knowing that it will get shoot it still shoots.
