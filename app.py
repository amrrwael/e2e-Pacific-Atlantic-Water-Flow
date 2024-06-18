from flask import Flask, request, render_template, jsonify
app = Flask(__name__)

class Solution:
    def pacificAtlantic(self, heights):
        if not heights or not heights[0]:
            return []

        ROWS, COLS = len(heights), len(heights[0])
        pac, atl = set(), set()

        def dfs(r, c, visit, prevHeight):
            if (
                (r, c) in visit
                or r < 0
                or c < 0
                or r >= ROWS
                or c >= COLS
                or heights[r][c] < prevHeight
            ):
                return
            visit.add((r, c))
            dfs(r + 1, c, visit, heights[r][c])
            dfs(r - 1, c, visit, heights[r][c])
            dfs(r, c + 1, visit, heights[r][c])
            dfs(r, c - 1, visit, heights[r][c])

        for c in range(COLS):
            dfs(0, c, pac, heights[0][c])
            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])

        for r in range(ROWS):
            dfs(r, 0, pac, heights[r][0])
            dfs(r, COLS - 1, atl, heights[r][COLS - 1])

        res = []
        for r in range(ROWS):
            for c in range(COLS):
                if (r, c) in pac and (r, c) in atl:
                    res.append([r, c])
        return res

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pacific_atlantic', methods=['POST'])
def pacific_atlantic():
    data = request.get_json()
    heights = data.get('heights', [])
    solution = Solution()
    result = solution.pacificAtlantic(heights)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
