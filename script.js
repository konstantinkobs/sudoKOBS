const app = new Vue({
	el: '.app',
	data: {
        data: null,
		grid: [],
		mask: [],
		solved: [],
		activeOption: 0,
        isEnd: false,
        isCorrect: true,
        level: "easy"
	},
	created: function () {
		fetch('generation/sudoko.json')
			.then((res) => res.json())
			.then((json) => {
                this.data = json;
				this.setLevel(this.level);
			});
	},
	methods: {
		fill: function (row, col) {
			if (this.start[row][col] == 0) {
                if (this.grid[row][col] == this.activeOption) {
                    this.grid[row][col] = 0;
				} else {
                    this.grid[row][col] = this.activeOption;
                }
                // we need to do this in order to update the app
                this.grid = [].concat(this.grid);
			}

			const g = JSON.stringify(this.grid);
			const s = JSON.stringify(this.solved);
			if (!g.includes('0')) {
				this.isEnd = true;

				if (g == s) {
                    this.isCorrect = true;
					// Let confetti rain for 5 seconds
					confetti.start(5000);
				} else {
                    this.isCorrect = false;

                    // Remove wrong inputs
                    for (let row = 0; row < 9; row++) {
                        for (let col = 0; col < 9; col++) {
                            if (this.grid[row][col] != this.solved[row][col]) {
                                this.grid[row][col] = 0;
                            }
                        }
                    }
                    this.grid = [].concat(this.grid);
				}
			}
		},
		restart: function () {
            this.grid = JSON.parse(JSON.stringify(this.start));
            this.isCorrect = false;
            this.isEnd = false;
		},
		show: function () {
			this.grid = JSON.parse(JSON.stringify(this.solved));
        },
        setLevel: function(level) {
            this.level = level;
            this.grid = JSON.parse(JSON.stringify(this.data[this.level]['start']));
			this.solved = JSON.parse(JSON.stringify(this.data[this.level]['solved']));
			// deep copy of the start data
			this.start = JSON.parse(JSON.stringify(this.data[this.level]['start']));
        }
    }
});