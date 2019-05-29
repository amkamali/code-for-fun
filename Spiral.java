public class Spiral {

	static int[] hStep = new int[]{1, 0, -1, 0};
	static int[] vStep = new int[]{0, 1, 0, -1,};

	static int[][] spiral(int n) {
		int row = 0;
		int col = 0;
		int direction = 0;	// 0: right, 1: down, 2: left, 3: up
		int cellNum = n * n;
		int[][] spr = new int[n][n];
		for (int counter = 1; counter <= cellNum; counter++) {
			spr[row][col] = counter;
			if (row + vStep[direction] >= n || col + hStep[direction] >= n
 			 || row + vStep[direction] < 0  || col + hStep[direction] < 0 
			 || spr[row + vStep[direction]][col + hStep[direction]] != 0) {
				direction = (direction + 1) % 4;
			}
			row += vStep[direction];
			col += hStep[direction];
		}
		return spr;
	}

	static void printSpiral(int[][] spr, int spiralSize) {
		for (int row = 0; row < spiralSize; row++) {
			for (int col = 0; col < spiralSize; col++) {		
				System.out.format("%5d ", spr[row][col]);
			}
			System.out.println("");
		}
	}

	public static void main(String[] args) {
		if (args.length != 1) {
			System.out.println("Usage: Spiral <size of the spiral>");
		} else {
			int spiralSize = Integer.parseInt(args[0]);
			int[][] spr = spiral(spiralSize);
			printSpiral(spr, spiralSize);
		}

	} 
}