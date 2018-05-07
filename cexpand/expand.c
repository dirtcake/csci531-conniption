#include <Python.h>
#include <stdlib.h>
#include <string.h>

static PyObject *board_class;

typedef struct {
	PyObject_HEAD
	Py_ssize_t index;
	PyObject *board_state;
	long board[7][6];
	long flipped_board[7][6];
	long player_turn;
	long flipped;
	long flips;
	long p1_flips;
	long p2_flips;
} ExpandState;

static void flip(long board[7][6]) {
	for (int c = 0; c < 7; c++) {
		// find the last nonempty row
		int max_row = 0;
		for (int r = 0; r < 6; r++) {
			if (board[c][r] == 0) {
				max_row = r-1;
			}
		}

		// reverse the row
		for (int r = 0; r < max_row/2; r++) {
			int temp = board[c][r];
			board[c][r] = board[c][max_row-r];
			board[c][max_row-r] = temp;
		}
	}
}

static PyObject *expand_new(PyTypeObject *type, PyObject *args, PyObject *kwargs) {

	PyObject *board_state;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "O", &board_state)) {
        return NULL;
	}

	ExpandState *expand_state = (ExpandState *)type->tp_alloc(type, 0);
	if (!board_state)
		return NULL;

	Py_INCREF(board_state);

	expand_state->board_state = board_state;
	expand_state->index = 0;
	expand_state->player_turn = PyLong_AsLong(PyObject_GetAttrString(board_state, "player_turn"));
	expand_state->flipped = PyLong_AsLong(PyObject_GetAttrString(board_state, "flipped"));
	expand_state->p1_flips = PyLong_AsLong(PyObject_GetAttrString(board_state, "p1_flips"));
	expand_state->p2_flips = PyLong_AsLong(PyObject_GetAttrString(board_state, "p2_flips"));

	if (expand_state->player_turn == 1) {
		expand_state->flips = PyLong_AsLong(PyObject_GetAttrString(board_state, "p1_flips"));
	} else {
		expand_state->flips = PyLong_AsLong(PyObject_GetAttrString(board_state, "p2_flips"));
	}

	PyObject *pyboard = PyObject_GetAttrString(board_state, "board");
	PyObject **items = PySequence_Fast_ITEMS(pyboard);

	PyObject **col;
	for (int c = 0; c < 7; c++) {
		col = PySequence_Fast_ITEMS(items[c]);
		for (int r = 0; r < 6; r++) {
			expand_state->board[c][r] = PyLong_AsLong(col[r]);
			expand_state->flipped_board[c][r] = PyLong_AsLong(col[r]);
		}
	}

	flip(expand_state->flipped_board);

	return (PyObject *)expand_state;
}

static void expand_dealloc(ExpandState *state) {
	Py_XDECREF(state);
	Py_TYPE(state)->tp_free(state);
}

static PyObject *build_object(long board[7][6], long player_turn, long p1_flips, long p2_flips, long flipped) {
	
	// build the board (list of lists)
	PyObject *cols[7];
	long b[7][6];
	memcpy(b, board, 42 * sizeof(long));
	for (int c = 0; c < 7; c++) {
		cols[c] = Py_BuildValue("[llllll]", b[c][0], b[c][1], b[c][2], b[c][3], b[c][4], b[c][5]);
	}
	PyObject *pyboard = Py_BuildValue("[OOOOOOO]", cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6]);

	PyObject *args = Py_BuildValue("Ollll", pyboard, player_turn, p1_flips, p2_flips, flipped);
	PyObject *BoardState = PyObject_GetAttrString(board_class, "BoardState");

	PyObject *ret = PyObject_CallObject(BoardState, args);
	return ret;
}

static PyObject *expand_next(ExpandState *state) {
	int index = state->index;
	state->index++;

	// place
	if (index < 7) {
		int i = index;
		for (int j = 0; j < 6; j++) {
			if (state->board[i][j] == 0) {
				state->board[i][j] = state->player_turn;
				PyObject *ret = build_object(state->board, state->player_turn % 2 + 1, state->p1_flips, state->p2_flips, 0);
				state->board[i][j] = 0;
				return ret;
			}
		}
	}

	// if there are no more flips or the board is flipped, skip flip+place
	if (state->flips == 0 || state->flipped) {
		index += 7;
	}

	// flip and place
	if (index < 14) {
		if (state->flips > 0 && !state->flipped) {
			int i = index % 7;
			for (int j = 0; j < 6; j++) {
				if (state->flipped_board[i][j] == 0) {
					state->flipped_board[i][j] = state->player_turn;
					PyObject *ret;
					if (state->player_turn == 1) {
						ret = build_object(state->flipped_board, state->player_turn % 2 + 1, state->p1_flips - 1, state->p2_flips, 0);
					} else {
						ret = build_object(state->flipped_board, state->player_turn % 2 + 1, state->p1_flips, state->p2_flips - 1, 0);
					}
					state->flipped_board[i][j] = 0;
					return ret;
				}
			}
		}
	}

	// if there are no more flips, skip place+flip
	if (state->flips == 0) {
		index += 7;
	}

	// place and flip
	if (index < 21) {
		int i = index % 7;
		for (int j = 0; j < 6; j++) {
			if (state->flipped_board[i][j] == 0) {
				for (int k = j; k > 0; k--) {
					state->flipped_board[i][k] = state->flipped_board[i][k-1];
				}
				state->flipped_board[i][0] = state->player_turn;
				PyObject *ret;
				if (state->player_turn == 1) {
					ret = build_object(state->flipped_board, state->player_turn % 2 + 1, state->p1_flips - 1, state->p2_flips, 1);
				} else {
					ret = build_object(state->flipped_board, state->player_turn % 2 + 1, state->p1_flips, state->p2_flips - 1, 1);
				}

				for (int k = 0; k < j; k++) {
					state->flipped_board[i][k] = state->flipped_board[i][k+1];
				}
				state->flipped_board[i][j] = 0;
				return ret;
			}
		}
	}

	// if there are no more flips or the board is flipped, skip flip+place+flip
	if (state->flips == 0 || state->flipped) {
		index += 7;
	}

	// flip place flip
	if (index < 28) {
		int i = index % 7;
		for (int j = 0; j < 6; j++) {
			if (state->board[i][j] == 0) {
				for (int k = 0; k > 0; k--) {
					state->board[i][k] = state->board[i][k-1];
				}
				state->board[i][0] = state->player_turn;
				PyObject *ret;

				if (state->player_turn == 1) {
					ret = build_object(state->board, state->player_turn % 2 + 1, state->p1_flips - 2, state->p2_flips, 1);
				} else {
					ret = build_object(state->board, state->player_turn % 2 + 1, state->p1_flips, state->p2_flips - 2, 1);
				}

				for (int k = 0; k < j; k++) {
					state->board[i][k] = state->board[i][k+1];
				}
				state->board[i][j] = 0;
				return ret;
			}
		}
	}

	// the iterator has been exhaused
	return NULL;
}


PyTypeObject PyExpand_Type = {
	PyVarObject_HEAD_INIT(&PyType_Type, 0)
	"expand",
	sizeof(ExpandState),
	0,
	(destructor)expand_dealloc,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	Py_TPFLAGS_DEFAULT,
	0,
	0,
	0,
	0,
	0,
	PyObject_SelfIter,
	(iternextfunc)expand_next,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	PyType_GenericAlloc,
	expand_new,
};


PyMODINIT_FUNC PyInit_expand(void) {
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "expand",
        "",
        -1,
    };

    PyObject *module = PyModule_Create(&moduledef);
    if (!module)
		return NULL;

	if (PyType_Ready(&PyExpand_Type) < 0)
		return NULL;

	Py_INCREF((PyObject *)&PyExpand_Type);
	PyModule_AddObject(module, "expand", (PyObject *)&PyExpand_Type);

	board_class = PyImport_ImportModule("board_class");
    return module;
}
