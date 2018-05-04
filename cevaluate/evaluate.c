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
                       1,  16,    0,  16,     256,    8,    0,    4,       -8,// 0100-0122
                //  0200 0201  0202 0210     0211  0212  0220  0221     0222
                      -1,   0,  -16,   0,       8,   -4,  -16,   -8,     -256,// 0200-0222
                //  1000 1001  1002 1010     1011  1012  1020  1021     1022
                       1,  16,    0,  16,     256,    8,    0,    4,       -8,// 1000-1022
                //  1100 1101  1102 1110     1111  1112  1120  1121     1122
                      16, 256,    8, 256, 1000000,  128,    8,  128,        0,// 1100-1122
                //  1200 1201  1202 1210     1211  1212  1220  1221     1222
                       0,   4,   -8,   4,     128,    0,   -8,    0,     -128,// 1200-1222
                //  2000 2001  2002 2010     2011  2012  2020  2021     2022
                      -1,   0,  -16,   0,       8,   -4,  -16,   -8,     -256,// 2000-2022
                //  2100 2101  2102 2110     2111  2112  2120  2121     2122
                       0,   8,   -4,   8,     128,    0,   -4,    0,     -128,// 2100-2122
                //  2200 2201  2202 2210     2211  2212  2220  2221     2222
                     -16,  -8, -256,  -8,       0, -128, -256, -128, -1000000 // 2200-2222
};

static PyObject *evaluate_evaluate_full(PyObject *self, PyObject *args)
{
	PyObject *board;
	int player;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "Oi", &board, &player)) {
        return NULL;
	}

	if (!PySequence_Check(board)) {
		return NULL;
	}

	PyObject *col[7];

	// get the columns
	for (int i = 0; i < 7; i++) {
		col[i] = PySequence_GetItem(board, i);
		// or not
		if (!PySequence_Check(col[i])) {
			for (int j = 0; j < 7; j++) {
				Py_XDECREF(col[i]);
			}
			return NULL;
		}
	}

	int total = 0;
	int index;
	// winner is set to player when player has a win.
	// this is to avoid one player's win cancelling the other when both have a win
	int winner = 0;
	for (int c = 0; c < 7; c++) {
		for (int r = 0; r < 6; r++) {
			long start = PyLong_AsLong(PySequence_GetItem(col[c], r)) * 27;

			if (r < 3) {
				index = start
					+ PyLong_AsLong(PySequence_GetItem(col[c], r+1)) * 9
					+ PyLong_AsLong(PySequence_GetItem(col[c], r+2)) * 3
					+ PyLong_AsLong(PySequence_GetItem(col[c], r+3));
				if ((evals[index] > 500000 && player == 1) || (evals[index] < -500000 && player == 2)) {
					winner = player;
				}
				total += evals[index];
			}

			if (c < 4) {
				index = start
					+ PyLong_AsLong(PySequence_GetItem(col[c+1], r)) * 9
					+ PyLong_AsLong(PySequence_GetItem(col[c+2], r)) * 3
					+ PyLong_AsLong(PySequence_GetItem(col[c+3], r));
				if ((evals[index] > 500000 && player == 1) || (evals[index] < -500000 && player == 2)) {
					winner = player;
				}
				total += evals[index];
				if (r < 3) {
					index = start
						+ PyLong_AsLong(PySequence_GetItem(col[c+1], r+1)) * 9
						+ PyLong_AsLong(PySequence_GetItem(col[c+2], r+2)) * 3
						+ PyLong_AsLong(PySequence_GetItem(col[c+3], r+3));
					if ((evals[index] > 500000 && player == 1) || (evals[index] < -500000 && player == 2)) {
						winner = player;
					}
					total += evals[index];
				} else {
					index = start
						+ PyLong_AsLong(PySequence_GetItem(col[c+1], r-1)) * 9
						+ PyLong_AsLong(PySequence_GetItem(col[c+2], r-2)) * 3
						+ PyLong_AsLong(PySequence_GetItem(col[c+3], r-3));
					if ((evals[index] > 500000 && player == 1) || (evals[index] < -500000 && player == 2)) {
						winner = player;
					}
					total += evals[index];
				}
			}
		}
	}

	if (player == 2) {
		total = -total;
	}

    /* Clean up. */
	for (int i = 0; i < 7; i++) {
		Py_XDECREF(col[i]);
	}

	// if player can win, ensure this isn't cancelled out by the other player's win
	if (winner == player) {
		total = 1000000;
	}

    /* Build the return value */
    PyObject *ret = Py_BuildValue("i", total);
    return ret;
}

