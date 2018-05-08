#include <Python.h>
#include <stdlib.h>

static char module_docstring[] =
    "This module provides an evaluation function.";
static char evaluate_full_docstring[] =
    "This module provides an evaluation function.";

static PyObject *evaluate_evaluate_full(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"evaluate_full", evaluate_evaluate_full, METH_VARARGS, evaluate_full_docstring},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC PyInit_evaluate(void)
{
    
    PyObject *module;
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "evaluate",
        module_docstring,
        -1,
        module_methods,
        NULL,
        NULL,
        NULL,
        NULL
    };
    module = PyModule_Create(&moduledef);
    if (!module) return NULL;

    return module;
}


static int evals[81] = {
                //  0000 0001  0002 0010     0011  0012  0020  0021     0022
                       0,   1,   -1,   1,      16,    0,   -1,    0,      -16,// 0000-0022
                //  0100 0101  0102 0110     0111  0112  0120  0121     0122
                       1,  16,    0,  16,     256,    0,    0,    0,       0,// 0100-0122
                //  0200 0201  0202 0210     0211  0212  0220  0221     0222
                      -1,   0,  -16,   0,       0,    0,  -16,    0,     -256,// 0200-0222
                //  1000 1001  1002 1010     1011  1012  1020  1021     1022
                       1,  16,    0,  16,     256,    0,    0,    0,       0,// 1000-1022
                //  1100 1101  1102 1110     1111  1112  1120  1121     1122
                      16, 256,    0, 256, 1000000,    0,    0,    0,       0,// 1100-1122
                //  1200 1201  1202 1210     1211  1212  1220  1221     1222
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 1200-1222
                //  2000 2001  2002 2010     2011  2012  2020  2021     2022
                      -1,   0,  -16,   0,       0,    0,  -16,    0,     -256,// 2000-2022
                //  2100 2101  2102 2110     2111  2112  2120  2121     2122
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 2100-2122
                //  2200 2201  2202 2210     2211  2212  2220  2221     2222
                     -16,   0, -256,   0,       0,    0, -256,    0, -1000000 // 2200-2222
};

static int evals_col[81] = {
                //  0000 0001  0002 0010     0011  0012  0020  0021     0022
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 0000-0022
                //  0100 0101  0102 0110     0111  0112  0120  0121     0122
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 0100-0122
                //  0200 0201  0202 0210     0211  0212  0220  0221     0222
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 0200-0222
                //  1000 1001  1002 1010     1011  1012  1020  1021     1022
                       1,   0,    0,   0,       0,    0,    0,    0,        0,// 1000-1022
                //  1100 1101  1102 1110     1111  1112  1120  1121     1122
                      16,   0,    0, 256, 1000000,    0,    0,    0,        0,// 1100-1122
                //  1200 1201  1202 1210     1211  1212  1220  1221     1222
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 1200-1222
                //  2000 2001  2002 2010     2011  2012  2020  2021     2022
                      -1,   0,    0,   0,       0,    0,    0,    0,        0,// 2000-2022
                //  2100 2101  2102 2110     2111  2112  2120  2121     2122
                       0,   0,    0,   0,       0,    0,    0,    0,        0,// 2100-2122
                //  2200 2201  2202 2210     2211  2212  2220  2221     2222
                     -16,   0,    0,   0,       0,    0, -256,    0, -1000000 // 2200-2222
};

static PyObject *evaluate_evaluate_full(PyObject *self, PyObject *args)
{
	PyObject *pyboard;
	int player;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "Oi", &pyboard, &player)) {
        return NULL;
	}

	if (!PySequence_Check(pyboard)) {
		return NULL;
	}

  long board[7][6];
  PyObject **cols = PySequence_Fast_ITEMS(pyboard);
  PyObject **col;

  // get the columns
  for (int c = 0; c < 7; c++) {
    col = PySequence_Fast_ITEMS(cols[c]);

    for (int r = 0; r < 6; r++) {
      board[c][r] = PyLong_AsLong(col[r]);
    }

  }

	int total = 0;
	int index;
	// winner is set to player when player has a win.
	// this is to avoid one player's win cancelling the other when both have a win
	int winner = 0;
	for (int c = 0; c < 7; c++) {
		for (int r = 0; r < 6; r++) {
			long start = board[c][r] * 27;

			if (r < 3) {
				index = start + board[c][r+1] * 9 + board[c][r+2] * 3 + board[c][r+3];
				total += evals_col[index];
			}

			if (c < 4) {
				index = start + board[c+1][r] * 9 + board[c+2][r] * 3 + board[c+3][r];
				total += evals[index];

				if (r < 3) {
					index = start + board[c+1][r+1] * 9 + board[c+2][r+2] * 3 + board[c+3][r+3];
					total += evals[index];
				} else {
					index = start + board[c+1][r-1] * 9 + board[c+2][r-2] * 3 + board[c+3][r-3];
					total += evals[index];
				}
			}

			if ((total > 1000000 && player == 1) || (total < -1000000 && player == 2)) {
				winner = player;
			}
		}
	}

	if (player == 2) {
		total = -total;
	}

	// if player can win, ensure this isn't cancelled out by the other player's win
	if (winner == player) {
		total = 1000000;
	}

    /* Build the return value */
    PyObject *ret = Py_BuildValue("i", total);
    return ret;
}

