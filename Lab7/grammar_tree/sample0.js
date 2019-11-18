derived_children = {
	"x A": [
		{ "name": "x", "isTerminal": true },
		{ "name": "A", "isTerminal": false },
	],
	"x B": [
		{ "name": "x", "isTerminal": true },
		{ "name": "B", "isTerminal": false },
	],
	"x": [
		{ "name": "x", "isTerminal": true },
	],
	"z B": [
		{ "name": "z", "isTerminal": true },
		{ "name": "B", "isTerminal": false },
	],
	"z": [
		{ "name": "z", "isTerminal": true },
	],
}

derivations = {
	"A": [
			{ "name": "x A" },
			{ "name": "x B" },
			{ "name": "x" },
		],
	"B": [
			{ "name": "z B" },
			{ "name": "z" },
		],
}

root = {
	"name": "A",
}