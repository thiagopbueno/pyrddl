from pyrddl import parser
from pyrddl.rddl import RDDL, Domain, Instance, NonFluents
from pyrddl.cpf import CPF

import unittest


with open('rddl/Reservoir.rddl', mode='r') as file:
    RESERVOIR = file.read()

with open('rddl/Mars_Rover.rddl', mode='r') as file:
    MARS_ROVER = file.read()


class TestRDDLlex(unittest.TestCase):

    def setUp(self):
        self.lexer = parser.RDDLlex()
        self.lexer.build()

    def test_newlines(self):
        self.lexer.input(RESERVOIR)
        for _ in self.lexer(): pass
        self.assertEqual(self.lexer._lexer.lineno, 147)

    def test_identifiers(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if tok.type == 'ID':
                self.assertIsInstance(tok.value, str)
                self.assertIn(tok.value[0], "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ")
                if len(tok.value) > 1:
                    for c in tok.value[1:-1]:
                        self.assertIn(c, "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ0123456789-_")
                    self.assertIn(tok.value[-1], "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ0123456789'")

    def test_reserved_words(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if tok.type == 'ID':
                self.assertNotIn(tok.value, self.lexer.reserved)
            if tok.value in self.lexer.reserved:
                self.assertEqual(tok.type, self.lexer.reserved[tok.value])

    def test_floating_point_numbers(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if tok.type == 'DOUBLE':
                self.assertIsInstance(tok.value, float)
            if isinstance(tok.value, float):
                self.assertEqual(tok.type, 'DOUBLE')

    def test_integer_numbers(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if tok.type == 'INTEGER':
                self.assertIsInstance(tok.value, int)
            if isinstance(tok.value, int):
                self.assertEqual(tok.type, 'INTEGER')

    def test_operators(self):
        op2tok = {
            '^': 'AND',
            '|': 'OR',
            '~': 'NOT',
            '+': 'PLUS',
            '*': 'TIMES',
            '.': 'DOT',
            '=>': 'IMPLY',
            '<=>': 'EQUIV',
            '~=': 'NEQ',
            '<=': 'LESSEQ',
            '<': 'LESS',
            '>=': 'GREATEREQ',
            '>': 'GREATER',
            '=': 'ASSIGN_EQUAL',
            '==': 'COMP_EQUAL',
            '/': 'DIV',
            '-': 'MINUS',
            ':': 'COLON',
            ';': 'SEMI',
            '$': 'DOLLAR_SIGN',
            '?': 'QUESTION',
            '&': 'AMPERSAND'
        }

        tok2op = {
            'AND': '^',
            'OR': '|',
            'NOT': '~',
            'PLUS': '+',
            'TIMES': '*',
            'DOT': '.',
            'IMPLY': '=>',
            'EQUIV': '<=>',
            'NEQ': '~=',
            'LESSEQ': '<=',
            'LESS': '<',
            'GREATEREQ': '>=',
            'GREATER': '>',
            'ASSIGN_EQUAL': '=',
            'COMP_EQUAL': '==',
            'DIV': '/',
            'MINUS': '-',
            'COLON': ':',
            'SEMI': ';',
            'DOLLAR_SIGN': '$',
            'QUESTION': '?',
            'AMPERSAND': '&'
        }

        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if tok.value in op2tok:
                self.assertEqual(tok.type, op2tok[tok.value])
            if tok.type in tok2op:
                self.assertEqual(tok.value, tok2op[tok.type])

    def test_delimiters(self):
        delim2tok = {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LCURLY',
            '}': 'RCURLY',
            ',': 'COMMA',
            '[': 'LBRACK',
            ']': 'RBRACK'
        }

        tok2delim = {
            'LPAREN': '(',
            'RPAREN': ')',
            'LCURLY': '{',
            'RCURLY': '}',
            'COMMA': ',',
            'LBRACK': '[',
            'RBRACK': ']'
        }

        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if tok.value in delim2tok:
                self.assertEqual(tok.type, delim2tok[tok.value])
            if tok.type in tok2delim:
                self.assertEqual(tok.value, tok2delim[tok.type])

    def test_variables(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if not isinstance(tok.value, str):
                continue

            if tok.type == 'VAR':
                self.assertIsInstance(tok.value, str)
                self.assertGreaterEqual(len(tok.value), 2)
                self.assertEqual(tok.value[0], '?')
                if len(tok.value) == 2:
                    self.assertIn(tok.value[1], "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ0123456789")
                else:
                    for c in tok.value[1:-1]:
                        self.assertIn(c, "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ0123456789-_")
                    self.assertIn(tok.value[-1], "abcdefghijklmnopqrstuvxwyzABCDEFGHIJKLMNOPQRSTUVXWYZ0123456789")

            if tok.value[0] == '?':
                self.assertEqual(tok.type, 'VAR')

    def test_ignore_whitespaces(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if isinstance(tok.value, str):
                self.assertNotIn(' ', tok.value)
                self.assertNotIn('\t', tok.value)

    def test_ignore_comments(self):
        self.lexer.input(RESERVOIR)
        for tok in self.lexer():
            if isinstance(tok.value, str):
                self.assertFalse(tok.value.startswith("//"))


class TestRDDLyacc(unittest.TestCase):

    def setUp(self):
        rddl = '''
        ////////////////////////////////////////////////////////////////////
        // The problem models the active maintenance of water levels in
        // a Reservoir system with uncertain rainfall and nonlinear
        // evaporation rates as a function of water level.  The objective
        // is to maintain all reservoir levels within a desired safe range.
        //
        // The state of each reservoir is the water level (rlevel).  The
        // actions are to set the outflows of each reservoir.  Rewards
        // are summed per reservoir and optimal when the water level is
        // within predefined upper and lower bounds.
        //
        // Author: Ga Wu, Buser Say inspired by Aswin Raghavan's RDDL model
        ////////////////////////////////////////////////////////////////////

        domain reservoir {
            requirements = {
                concurrent,           // x and y directions move independently and simultaneously
                reward-deterministic, // this domain does not use a stochastic reward
                intermediate-nodes,   // this domain uses intermediate pvariable nodes
                constrained-state     // this domain uses state constraints
            };

            types {
                res: object;
                picture-point : object;
                x_pos : object;
                y_pos : object;
                crowdlevel : {@low, @med, @high};
                enum_level : {@low, @high}; // An enumerated type
            };

            pvariables {

                // Constants
                MAX_RES_CAP(res): { non-fluent, real, default = 100.0 }; // Beyond this amount, water spills over
                UPPER_BOUND(res): { non-fluent, real, default = 80.0 };  // The upper bound for a safe reservoir level
                LOWER_BOUND(res): { non-fluent, real, default = 20.0 };  // The lower bound for a safe reservoir level
                RAIN_SHAPE(res):  { non-fluent, real, default = 25.0 };  // Gamma shape parameter for rainfall
                RAIN_SCALE(res):  { non-fluent, real, default = 25.0 };  // Gamma scale paramater for rainfall
                DOWNSTREAM(res,res): { non-fluent, bool, default = false }; // Indicates 2nd res is downstream of 1st res
                SINK_RES(res):    { non-fluent, bool, default = false }; // This is a "sink" water source (sea, ocean) 
                MAX_WATER_EVAP_FRAC_PER_TIME_UNIT: { non-fluent, real, default = 0.05 }; // Maximum fraction of evaporation
                LOW_PENALTY(res) : { non-fluent, real, default =  -5.0 }; // Penalty per unit of level < LOWER_BOUND
                HIGH_PENALTY(res): { non-fluent, real, default = -10.0 }; // Penalty per unit of level > UPPER_BOUND
                PICT_XPOS(picture-point)   : { non-fluent, real, default = 0.0 };
                PICT_YPOS(picture-point)   : { non-fluent, real, default = 0.0 };

                // State fluents
                rlevel(res): {state-fluent, real, default = 50.0 }; // Reservoir level for res
                xPos : { state-fluent, real, default = 0.0 };
                yPos : { state-fluent, real, default = 0.0 };
                time : { state-fluent, real, default = 0.0 };
                picTaken(picture-point) : { state-fluent, bool, default = false };

                // Action fluents
                outflow(res): { action-fluent, real, default = 0.0 }; // Action to set outflow of res
                xMove       : { action-fluent, real, default = 0.0 };
                yMove       : { action-fluent, real, default = 0.0 };
                snapPicture : { action-fluent, bool, default = false };

                // Intermediate fluents
                evaporated(res): {interm-fluent, real, level=1}; // How much evaporates from res in this time step?
                rainfall(res):   {interm-fluent, real, level=1}; // How much rainfall is there in this time step?
                overflow(res):   {interm-fluent, real, level=1}; // Is there any excess overflow (over the rim)?
            };

            cpfs {
                evaporated(?r) = MAX_WATER_EVAP_FRAC_PER_TIME_UNIT
                                 *[(-11.8 * rlevel(?r)*rlevel(?r))/(MAX_RES_CAP(?r)*MAX_RES_CAP(?r) - 5)]
                                 * (+ rlevel(?r));

                // Consider MAX_RES_CAP=90, rlevel=100, outflow=4, then the excess overflow is 6 units
                // Consider MAX_RES_CAP=100, rlevel=90, outflow=4, then the excess overflow is 0 units
                overflow(?r) = max[0, rlevel(?r) - outflow(?x) - MAX_RES_CAP(?r, ?t)];

                rlevel'(?r) = rlevel(?r) + rainfall(?r) + (- evaporated(?r)) - outflow(?r) + [- overflow(?r)];

                distance(?r) = sqrt[pow[(location(?l)-CENTER(?l)),2]];
                scalefactor = 2.0/(1.0+exp[-2*distance])-0.99;

                rainfall(?r, ?s) = Gamma(RAIN_SHAPE(?r, ?s) - (- 2), 0.1 * RAIN_SCALE(?s));

                xPos' = xPos + xMove + Normal(0.0, MOVE_VARIANCE_MULT*abs[xMove]);
                yPos' = cos[yPos + exp[yMove + (-Normal(1.0, abs[yMove] - (10 * MOVE_VARIANCE_MULT)))]];

                // Choose a level with following probabilities
                i2 = Discrete(enum_level,
                                @low : 0.5 + i1,
                                @high : 0.3,
                                @medium : - i1 + 0.2
                            );

                i1 = KronDelta(p + Bernoulli( (p + q + r)/3.0 ) + r);  // Just set i1 to a count of true state variables

                picTaken'(?p) = picTaken(?p) == true | ~notPicTaken(?p) &
                        [~snapPicture ~= false ^ (time <= MAX_TIME)
                         & (PICT_ERROR_ALLOW(?p) > abs[xPos - PICT_XPOS(?p)])
                         ^ ~(abs[yPos - PICT_YPOS(?p)] == PICT_ERROR_ALLOW(?p))];

                time' = if (snapPicture)
                    then (time + 0.25)
                    else (time + abs[xMove] + abs[yMove]);

                j2 = Discrete(enum_level,
                        @high : 0.3,
                        @low : if (i1 >= 2) then 0.5 else 0.2
                    );

                // Conditional linear stochastic equation
                o2 = switch (i2) {
                    case @high   : i1 + 3.0 + Normal(0.0, i1*i1/4.0),
                    case @medium : -i2 + 2 + Normal(1.0, i2*i1/2.0)
                };

                o3 = switch (i2) {
                    case @high   : i1 + 3.0 + Normal(0.0, i1*i1/4.0),
                    case @medium : -i2 + 2 + Normal(1.0, i2*i1/2.0),
                    default : -Normal(1.0, 0.0) * (-16.0)
                };

                rlevel2'(?r) = sum_{?up : res} [DOWNSTREAM(?up,?r) * (outflow(?up) + overflow(?up))];

                rlevel3'(?r) = rlevel(?r) + rainfall(?r) - evaporated(?r) - outflow(?r) - overflow(?r)
                      + sum_{?up : res} [DOWNSTREAM(?up,?r)*(outflow(?up) + overflow(?up))];

                rlevel4'(?r) = rlevel(?r) + rainfall(?r) - evaporated(?r) - outflow(?r)
                      + sum_{?up : res} [DOWNSTREAM(?up,?r)*(outflow(?up) + overflow(?up))]
                      - overflow(?r);

                rlevel5'(?r) = rlevel(?r) + rainfall(?r) - evaporated(?r) - outflow(?r)
                      + (sum_{?up : res} [DOWNSTREAM(?up,?r)*(outflow(?up) + overflow(?up))])
                      - overflow(?r);

                rlevel6'(?r) = max_{?up : res, ?down : res2} [DOWNSTREAM(?up,?down) * outflow(?up) + overflow(?up)];

                rlevel7'(?r) = rlevel(?r) + rainfall(?r) - evaporated(?r) - outflow(?r)
                      + sum_{?up : res1, ?down : res} [DOWNSTREAM(?up,?down)*(outflow(?up) + overflow(?up))]
                      - overflow(?r);


                // skill_teaching_mdp.rddl
                hintedRight'(?s) =
                    KronDelta( [forall_{?s3: skill} ~updateTurn(?s3)] ^
                                giveHint(?s) ^
                                forall_{?s2: skill}[PRE_REQ(?s2, ?s) => proficiencyHigh(?s2)] );

                hintDelayVar'(?s) =
                    KronDelta( [forall_{?s2: skill} ~updateTurn(?s2)] ^ giveHint(?s) );

                // crossing_traffic_mdp.rddl
                robot-at'(?x,?y) =
                    if ( exists_{?x2 : xpos, ?y2 : ypos} [ GOAL(?x2,?y2) ^ robot-at(?x2,?y2)  ] )
                    then
                        KronDelta(false) // because of fall-through we know (?x,y) != (?x2,?y2)
                    // Check for legal robot movement (robot disappears if at an obstacle)
                    else if ( move-north ^ exists_{?y2 : ypos} [ NORTH(?y2,?y) ^ robot-at(?x,?y2) ^ ~obstacle-at(?x,?y2) ] )
                    then
                        KronDelta(true) // robot moves to this location
                    else
                        false;

            };

            reward =
                    // Mars_Rover.rddl
                    sum_{?p : picture-point} [ (~picTaken(?p) ^ picTaken'(?p)) * PICT_VALUE(?p) ] +

                    // Reservoir.rddl
                    sum_{?r: res} [if (rlevel'(?r)>=LOWER_BOUND(?r) ^ (rlevel'(?r)<=UPPER_BOUND(?r)))
                                    then 0
                                    else if (rlevel'(?r)<=LOWER_BOUND(?r))
                                        then LOW_PENALTY(?r)*(LOWER_BOUND(?r)-rlevel'(?r))
                                        else HIGH_PENALTY(?r)*(rlevel'(?r)-UPPER_BOUND(?r))] +

                    // Navigation_Radius.rddl
                    - sum_{?l: dim}[abs[GOAL(?l) - location(?l)]] +

                    // game_of_life_mdp.rddl
                    sum_{?x : x_pos, ?y : y_pos} [alive(?x,?y) - set(?x,?y)] +

                    // recon_mdp.rddl
                    [sum_{?o : obj}
                        (GOOD_PIC_WEIGHT *
                        [ ~pictureTaken(?o) ^ lifeDetected(?o) ^ exists_{?x : x_pos, ?y : y_pos, ?a: agent, ?t: tool} [agentAt(?a, ?x, ?y) ^ objAt(?o, ?x, ?y) ^ useToolOn(?a, ?t, ?o) ^ CAMERA_TOOL(?t) ^ ~damaged(?t)]])
                    ] +
                    [sum_{?o : obj}
                        -(BAD_PIC_WEIGHT *
                        [ ~lifeDetected(?o) ^ exists_{?x : x_pos, ?y : y_pos, ?a: agent, ?t: tool} [agentAt(?a, ?x, ?y) ^ objAt(?o, ?x, ?y) ^ useToolOn(?a, ?t, ?o) ^ CAMERA_TOOL(?t)]])
                    ] -

                    // navigation_mdp.rddl
                    [sum_{?x : xpos, ?y : ypos} -(GOAL(?x,?y) ^ ~robot-at(?x,?y))] -

                    // elevators_mdp.rddl
                    [sum_{?e: elevator} [
                    -ELEVATOR-PENALTY-RIGHT-DIR * (person-in-elevator-going-up(?e) ^ elevator-dir-up(?e))
                    ]] +
                    [sum_{?e: elevator} [
                        -ELEVATOR-PENALTY-RIGHT-DIR * (person-in-elevator-going-down(?e) ^ ~elevator-dir-up(?e))
                    ]] +
                    [sum_{?e: elevator} [
                        -ELEVATOR-PENALTY-WRONG-DIR * (person-in-elevator-going-up(?e) ^ ~elevator-dir-up(?e))
                    ]] +
                    [sum_{?e: elevator} [
                        -ELEVATOR-PENALTY-WRONG-DIR * (person-in-elevator-going-down(?e) ^ elevator-dir-up(?e))
                    ]] +
                    [sum_{?f: floor} [
                        - person-waiting-up(?f) - person-waiting-down(?f)
                    ]] +

                    // traffic_mdp.rddl
                    sum_{?c : cell} -[occupied(?c) ^ exists_{?c2 : cell} (FLOWS-INTO-CELL(?c2, ?c) ^ occupied(?c2))] +

                    // skill_teaching_mdp.rddl
                    [sum_{?s : skill} [SKILL_WEIGHT(?s) * proficiencyHigh(?s)]] + [sum_{?s : skill} -[SKILL_WEIGHT(?s) * ~proficiencyMed(?s)]]
                    ;

            action-preconditions {

                // Mars_Rover.rddl
                // Cannot snap a picture and move at the same time
                snapPicture => ((xMove == 0.0) ^ (yMove == 0.0));

                // Reservoir.rddl
                forall_{?r : res} outflow(?r) <= rlevel(?r);
                forall_{?r : res} outflow(?r) >= 0;

            };

            state-action-constraints {

                // Navigation_Radius.rddl
                forall_{?l:dim} move(?l)<=MAXACTIONBOUND(?l);
                forall_{?l:dim} move(?l)>=MINACTIONBOUND(?l);
                forall_{?l:dim} location(?l)<=MAXMAZEBOUND(?l);
                forall_{?l:dim} location(?l)>=MINMAZEBOUND(?l);

                // recon_mdp.rddl
                (sum_{?t: tool}[WATER_TOOL(?t)])  >= 1;
                (sum_{?t: tool}[CAMERA_TOOL(?t)]) >= 1;
                (sum_{?t: tool}[LIFE_TOOL(?t)])   >= 1;

                // crossing_traffic_mdp.rddl
                // Robot at exactly one position
                [sum_{?x : xpos, ?y : ypos} robot-at(?x,?y)] <= 1;

                // EAST, WEST, NORTH, SOUTH defined properly (unique and symmetric)
                forall_{?x1 : xpos} [(sum_{?x2 : xpos} WEST(?x1,?x2)) <= 1];
                forall_{?x1 : xpos} [(sum_{?x2 : xpos} EAST(?x1,?x2)) <= 1];
                forall_{?y1 : ypos} [(sum_{?y2 : ypos} NORTH(?y1,?y2)) <= 1];
                forall_{?y1 : ypos} [(sum_{?y2 : ypos} SOUTH(?y1,?y2)) <= 1];
                forall_{?x1 : xpos, ?x2 : xpos} [ EAST(?x1,?x2) <=> WEST(?x2,?x1) ];
                forall_{?y1 : ypos, ?y2 : ypos} [ SOUTH(?y1,?y2) <=> NORTH(?y2,?y1) ];

                // Definition verification
                [ sum_{?x : xpos} MIN-XPOS(?x) ] == 1;
                [ sum_{?x : xpos} MAX-XPOS(?x) ] == 1;
                [ sum_{?y : ypos} MIN-YPOS(?y) ] == 1;
                [ sum_{?y : ypos} MAX-YPOS(?y) ] == 1;
                [ sum_{?x : xpos, ?y : ypos} GOAL(?x,?y) ] == 1;

                // elevators_mdp.rddl
                // Can check uniqueness constraint in many ways, but for simulator easiest
                // is just to count.
                forall_{?e : elevator} ([sum_{?f: floor} elevator-at-floor(?e, ?f)] == 1);

                // Max of one action per elevator.
                forall_{?e : elevator} [(open-door-going-up(?e) + open-door-going-down(?e) + close-door(?e) + move-current-dir(?e)) <= 1];

                // All floors except top and bottom must have one adjacent floor above/below
                forall_{?f : floor} [ TOP-FLOOR(?f) | (sum_{?fup : floor} ADJACENT-UP(?f,?fup)) == 1 ];
                forall_{?f : floor} [ BOTTOM-FLOOR(?f) | (sum_{?fdown : floor} ADJACENT-UP(?fdown,?f)) == 1 ];

                // game_of_life_mdp.rddl
                forall_{?x : x_pos, ?y : y_pos} [(NOISE-PROB(?x,?y) >= 0.0) ^ (NOISE-PROB(?x,?y) <= 1.0)];

            };

            state-invariants {

                // Reservoir.rddl
                forall_{?r : res} rlevel(?r) >= 0;
                forall_{?up : res} (sum_{?down : res} DOWNSTREAM(?up,?down)) <= 1;

                // traffic_control_ctm.rddl2
                // ensure exactly two cells flow into a merge cell
                forall_{?c : cell} [MERGE-CELL(?c)
                        => ((sum_{?c1 : cell} NEXT(?c1, ?c)) == 2)];
                // ensure a diverge cell flows into exactly two cells
                forall_{?c : cell} [DIVERGE-CELL(?c)
                        => ((sum_{?c2 : cell} NEXT(?c, ?c2)) == 2)];
                // ensure other (normal) cells flow into exactly one cell
                forall_{?c : cell} [(~DIVERGE-CELL(?c) ^ ~MERGE-CELL(?c) ^ ~LAST(?c))
                        => ((sum_{?c2 : cell} NEXT(?c, ?c2)) == 1)];
            };

        }

        non-fluents res8 {
            domain = reservoir;
            objects{
                res: {t1,t2,t3,t4,t5,t6,t7,t8};
                dim: {x,y};
                picture-point : {p1, p2, p3};
            };

            non-fluents {
                MAX_TIME = 12;
                MOVE_VARIANCE_MULT = 0.00001;
                RAIN_SHAPE(t1) = 0.0;
                RAIN_SCALE(t2,t2) = 5.0;
                RAIN_SCALE(t7) = 25.0;
                RAIN_SHAPE(t8, t7) = 1.0;
                RAIN_SCALE(t8) = 30.0;
                MAX_RES_CAP(t3) = 200.0;
                UPPER_BOUND(t3, t5) = -180.0;
                MAX_RES_CAP(t4) = 300.2;
                DOWNSTREAM(t1,t6);
                DOWNSTREAM(t2,t3);
                DOWNSTREAM(t3, t5);
                DOWNSTREAM(t4,t8);
                DOWNSTREAM(t5,t7);
                DOWNSTREAM(t6,t7);
                DOWNSTREAM(t7,t8);
                SINK_RES(t8);
            };
        }

        instance inst_reservoir_res8 {
            domain = reservoir;
            non-fluents = res8;
            init-state{
                rlevel(t1) = 75.0;
                rlevel(t1, t2) = -75;
                location(x) = 1.0;
                location(y) = 2;
                xPos = 0.0;
                yPos = 0.0;
                time = 0.0;
                picTaken(p1) = true;
                picTaken(p3) = false;
            };
            // State-action constraints above are sufficient
            max-nondef-actions = pos-inf;

            horizon = 40;

            discount = 0.9;
        }
        '''
        self.parser = parser.RDDLParser()
        self.parser.build()
        self.rddl = self.parser.parse(rddl)

    def test_rddl(self):
        self.assertIsInstance(self.rddl, RDDL)
        self.assertIsInstance(self.rddl.domain, Domain)
        self.assertIsInstance(self.rddl.instance, Instance)
        self.assertIsInstance(self.rddl.non_fluents, NonFluents)

    def test_domain_block(self):
        domain = self.rddl.domain
        self.assertIsInstance(domain, Domain)
        self.assertEqual(domain.name, 'reservoir')

    def test_requirements_section(self):
        requirements = self.rddl.domain.requirements
        self.assertListEqual(requirements, ['concurrent', 'reward-deterministic', 'intermediate-nodes', 'constrained-state'])

    def test_types_section(self):
        types = self.rddl.domain.types
        expected = [
            ('res', 'object'),
            ('picture-point', 'object'),
            ('x_pos', 'object'),
            ('y_pos', 'object'),
            ('crowdlevel', ['@low', '@med', '@high']),
            ('enum_level', ['@low', '@high'])
        ]
        for t in expected:
            self.assertIn(t, types)

    def test_pvariables_section(self):
        pvariables = self.rddl.domain.pvariables

        expected = {
            'MAX_RES_CAP': { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' : 100.0 },
            'UPPER_BOUND': { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' : 80.0 },
            'LOWER_BOUND': { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' : 20.0 },
            'RAIN_SHAPE':  { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' : 25.0 },
            'RAIN_SCALE':  { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' : 25.0 },
            'DOWNSTREAM':  { 'params': ['res', 'res'], 'type': 'non-fluent', 'range': 'bool', 'default' : False },
            'SINK_RES':    { 'params': ['res'], 'type': 'non-fluent', 'range': 'bool', 'default' : False },
            'MAX_WATER_EVAP_FRAC_PER_TIME_UNIT': { 'params': [], 'type': 'non-fluent', 'range': 'real', 'default' : 0.05 },
            'LOW_PENALTY' : { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' :  -5.0 },
            'HIGH_PENALTY': { 'params': ['res'], 'type': 'non-fluent', 'range': 'real', 'default' : -10.0 },
            'PICT_XPOS'   : { 'params': ['picture-point'], 'type': 'non-fluent', 'range': 'real', 'default': 0.0 },
            'PICT_YPOS'   : { 'params': ['picture-point'], 'type': 'non-fluent', 'range': 'real', 'default': 0.0 },
            'rlevel': { 'params': ['res'], 'type': 'state-fluent', 'range': 'real', 'default': 50.0 },
            'xPos' : { 'params': [], 'type': 'state-fluent', 'range': 'real', 'default': 0.0 },
            'yPos' : { 'params': [], 'type': 'state-fluent', 'range': 'real', 'default': 0.0 },
            'time' : { 'params': [], 'type': 'state-fluent', 'range': 'real', 'default': 0.0 },
            'picTaken' : { 'params': ['picture-point'], 'type': 'state-fluent', 'range': 'bool', 'default': False },
            'outflow'     : { 'params': ['res'], 'type': 'action-fluent', 'range': 'real', 'default': 0.0 },
            'xMove'       : { 'params': [], 'type': 'action-fluent', 'range': 'real', 'default': 0.0 },
            'yMove'       : { 'params': [], 'type': 'action-fluent', 'range': 'real', 'default': 0.0 },
            'snapPicture' : { 'params': [], 'type': 'action-fluent', 'range': 'bool', 'default': False },
            'evaporated': { 'params': ['res'], 'type': 'interm-fluent', 'range': 'real', 'level': 1},
            'rainfall':   { 'params': ['res'], 'type': 'interm-fluent', 'range': 'real', 'level': 1},
            'overflow':   { 'params': ['res'], 'type': 'interm-fluent', 'range': 'real', 'level': 1}
        }

        for pvar in pvariables:
            pvar_params = expected[pvar.name]['params']
            pvar_type = expected[pvar.name]['type']
            pvar_range = expected[pvar.name]['range']
            pvar_default = expected[pvar.name]['default'] if pvar_type != 'interm-fluent' else None
            pvar_level = expected[pvar.name]['level'] if pvar_type == 'interm-fluent' else None

            # name
            self.assertIn(pvar.name, expected)

            # params
            if len(pvar_params) == 0:
                self.assertIsNone(pvar.param_types)
            else:
                self.assertListEqual(pvar.param_types, pvar_params)

            # type
            if pvar_type == 'non-fluent':
                self.assertEqual(pvar.fluent_type, 'non-fluent')
            elif pvar_type == 'state-fluent':
                self.assertEqual(pvar.fluent_type, 'state-fluent')
            elif pvar_type == 'action-fluent':
                self.assertEqual(pvar.fluent_type, 'action-fluent')
            elif pvar_type == 'interm-fluent':
                self.assertEqual(pvar.fluent_type, 'interm-fluent')

            # range
            self.assertEqual(pvar.range, pvar_range)

            # default value
            if pvar_type != 'interm-fluent':
                self.assertAlmostEqual(pvar.default, pvar_default)
                if pvar.range == 'bool':
                    self.assertIsInstance(pvar.default, bool)
                elif pvar.range == 'real':
                    self.assertIsInstance(pvar.default, float)
                elif pvar.range == 'int':
                    self.assertIsInstance(pvar.default, int)

            # level
            if pvar_type == 'interm-fluent':
                self.assertEqual(pvar.level, pvar_level)
                self.assertIsInstance(pvar.level, int)

    def test_cpfs_section(self):
        header, cpfs = self.rddl.domain.cpfs
        self.assertEqual(header, 'cpfs')
        for cpf in cpfs:
            self.assertEqual(cpf.pvar[0], 'pvar_expr')

        ast = {
            'evaporated': [
                '*',
                '*',
                ('MAX_WATER_EVAP_FRAC_PER_TIME_UNIT', None),
                '/',
                '*',
                '*',
                '-',
                11.8,
                ('rlevel', ['?r']),
                ('rlevel', ['?r']),
                '-',
                '*',
                ('MAX_RES_CAP', ['?r']),
                ('MAX_RES_CAP', ['?r']),
                5,
                '+',
                ('rlevel', ['?r'])
            ],
            "rlevel'": [
                '+',
                '-',
                '+',
                '+',
                ('rlevel', ['?r']),
                ('rainfall', ['?r']),
                '-',
                ('evaporated', ['?r']),
                ('outflow', ['?r']),
                '-',
                ('overflow', ['?r'])
            ],
            'overflow': [
                'max',
                0,
                '-',
                '-',
                ('rlevel', ['?r']),
                ('outflow', ['?x']),
                ('MAX_RES_CAP', ['?r', '?t'])
            ],
            'distance': [
                'sqrt',
                'pow',
                '-',
                ('location', ['?l']),
                ('CENTER', ['?l']),
                2
            ],
            'scalefactor': [
                '-',
                '/',
                2.0,
                '+',
                1.0,
                'exp',
                '*',
                '-',
                2,
                ('distance', None),
                0.99
            ],
            'rainfall': [
                'Gamma',
                '-',
                ('RAIN_SHAPE', ['?r', '?s']),
                '-',
                2,
                '*',
                0.1,
                ('RAIN_SCALE', ['?s'])
            ],
            "xPos'": [
                '+',
                '+',
                ('xPos', None),
                ('xMove', None),
                'Normal',
                0.0,
                '*',
                ('MOVE_VARIANCE_MULT', None),
                'abs',
                ('xMove', None)
            ],
            "yPos'": [
                'cos',
                '+',
                ('yPos', None),
                'exp',
                '+',
                ('yMove', None),
                '-',
                'Normal',
                1.0,
                '-',
                'abs',
                ('yMove', None),
                '*',
                10,
                ('MOVE_VARIANCE_MULT', None)
            ],
            'i1': [
                'KronDelta',
                '+',
                '+',
                ('p', None),
                'Bernoulli',
                '/',
                '+',
                '+',
                ('p', None),
                ('q', None),
                ('r', None),
                3.0,
                ('r', None)
            ],
            'i2': [
                'Discrete',
                'enum_level',
                '@low',
                '+',
                0.5,
                ('i1', None),
                '@high',
                0.3,
                '@medium',
                '+',
                '-',
                ('i1', None),
                0.2
            ],
            "picTaken'": [
                '|',
                '==',
                ('picTaken', ['?p']),
                True,
                '&',
                '~',
                ('notPicTaken', ['?p']),
                '^',
                '&',
                '^',
                '~=',
                '~',
                ('snapPicture', None),
                False,
                '<=',
                ('time', None),
                ('MAX_TIME', None),
                '>',
                ('PICT_ERROR_ALLOW', ['?p']),
                'abs',
                '-',
                ('xPos', None),
                ('PICT_XPOS', ['?p']),
                '~',
                '==',
                'abs',
                '-',
                ('yPos', None),
                ('PICT_YPOS', ['?p']),
                ('PICT_ERROR_ALLOW', ['?p'])
            ],
            "time'": [
                'if',
                ('snapPicture', None),
                '+',
                ('time', None),
                0.25,
                '+',
                '+',
                ('time', None),
                'abs',
                ('xMove', None),
                'abs',
                ('yMove', None)
            ],
            'j2': [
                'Discrete',
                'enum_level',
                '@high',
                0.3,
                '@low',
                'if',
                '>=',
                ('i1', None),
                2,
                0.5,
                0.2
            ],
            'o2': [
                'switch',
                ('i2', None),
                '@high',
                '+',
                '+',
                ('i1', None),
                3.0,
                'Normal',
                0.0,
                '/',
                '*',
                ('i1', None),
                ('i1', None),
                4.0,
                '@medium',
                '+',
                '+',
                '-',
                ('i2', None),
                2,
                'Normal',
                1.0,
                '/',
                '*',
                ('i2', None),
                ('i1', None),
                2.0
            ],
            'o3': [
                'switch',
                ('i2', None),
                '@high',
                '+',
                '+',
                ('i1', None),
                3.0,
                'Normal',
                0.0,
                '/',
                '*',
                ('i1', None),
                ('i1', None),
                4.0,
                '@medium',
                '+',
                '+',
                '-',
                ('i2', None),
                2,
                'Normal',
                1.0,
                '/',
                '*',
                ('i2', None),
                ('i1', None),
                2.0,
                'default',
                '*',
                '-',
                'Normal',
                1.0,
                0.0,
                '-',
                16.0
            ],
            "rlevel2'": [
                'sum',
                ('?up', 'res'),
                '*',
                ('DOWNSTREAM', ['?up', '?r']),
                '+',
                ('outflow', ['?up']),
                ('overflow', ['?up'])
            ],
            "rlevel3'": [
                '+',
                '-',
                '-',
                '-',
                '+',
                ('rlevel', ['?r']),
                ('rainfall', ['?r']),
                ('evaporated', ['?r']),
                ('outflow', ['?r']),
                ('overflow', ['?r']),
                'sum',
                ('?up', 'res'),
                '*',
                ('DOWNSTREAM', ['?up', '?r']),
                '+',
                ('outflow', ['?up']),
                ('overflow', ['?up'])
            ],
            "rlevel4'": [
                '+',
                '-',
                '-',
                '+',
                ('rlevel', ['?r']),
                ('rainfall', ['?r']),
                ('evaporated', ['?r']),
                ('outflow', ['?r']),
                'sum',
                ('?up', 'res'),
                '-',
                '*',
                ('DOWNSTREAM', ['?up', '?r']),
                '+',
                ('outflow', ['?up']),
                ('overflow', ['?up']),
                ('overflow', ['?r'])
            ],
            "rlevel5'": [
                '-',
                '+',
                '-',
                '-',
                '+',
                ('rlevel', ['?r']),
                ('rainfall', ['?r']),
                ('evaporated', ['?r']),
                ('outflow', ['?r']),
                'sum',
                ('?up', 'res'),
                '*',
                ('DOWNSTREAM', ['?up', '?r']),
                '+',
                ('outflow', ['?up']),
                ('overflow', ['?up']),
                ('overflow', ['?r'])
            ],
            "rlevel6'": [
                'max',
                ('?up', 'res'),
                ('?down', 'res2'),
                '+',
                '*',
                ('DOWNSTREAM', ['?up', '?down']),
                ('outflow', ['?up']),
                ('overflow', ['?up'])
            ],
            "rlevel7'": [
                '+',
                '-',
                '-',
                '+',
                ('rlevel', ['?r']),
                ('rainfall', ['?r']),
                ('evaporated', ['?r']),
                ('outflow', ['?r']),
                'sum',
                ('?up', 'res1'),
                ('?down', 'res'),
                '-',
                '*',
                ('DOWNSTREAM', ['?up', '?down']),
                '+',
                ('outflow', ['?up']),
                ('overflow', ['?up']),
                ('overflow', ['?r'])
            ],
            "hintedRight'": [
                'KronDelta',
                '^',
                '^',
                'forall',
                ('?s3', 'skill'),
                '~',
                ('updateTurn', ['?s3']),
                ('giveHint', ['?s']),
                'forall',
                ('?s2', 'skill'),
                '=>',
                ('PRE_REQ', ['?s2', '?s']),
                ('proficiencyHigh', ['?s2'])
            ],
            "hintDelayVar'": [
                'KronDelta',
                '^',
                'forall',
                ('?s2', 'skill'),
                '~',
                ('updateTurn', ['?s2']),
                ('giveHint', ['?s'])
            ],
            "robot-at'": [
                'if',
                'exists',
                ('?x2', 'xpos'),
                ('?y2', 'ypos'),
                '^',
                ('GOAL', ['?x2', '?y2']),
                ('robot-at', ['?x2', '?y2']),
                'KronDelta',
                False,
                'if',
                '^',
                ('move-north', None),
                'exists',
                ('?y2', 'ypos'),
                '^',
                '^',
                ('NORTH', ['?y2', '?y']),
                ('robot-at', ['?x', '?y2']),
                '~',
                ('obstacle-at', ['?x', '?y2']),
                'KronDelta',
                True,
                False
            ]
        }

        for cpf in cpfs:

            pvar = cpf.pvar[1][0]
            self.assertIn(pvar, ast)

            expected = ast[pvar]
            i = 0

            stack = [cpf.expr]
            while len(stack) > 0:
                expr = stack.pop()
                if expr[0] == 'pvar_expr':
                    self.assertEqual(expr[1], expected[i])
                elif expr[0] == 'number':
                    if isinstance(expr[1], int):
                        self.assertEqual(expr[1], expected[i])
                    else:
                        self.assertAlmostEqual(expr[1], expected[i])
                elif expr[0] == 'boolean':
                    self.assertEqual(expr[1], expected[i])
                elif expr[0] == 'func':
                    self.assertEqual(expr[1][0], expected[i])
                    for subexpr in expr[1][1][::-1]:
                        stack.append(subexpr)
                elif expr[0] == 'enum_type':
                    self.assertEqual(expr[1], expected[i])
                elif expr[0] == 'typed_var':
                    self.assertEqual(expr[1], expected[i])
                elif expr[0] == 'lconst':
                    self.assertEqual(expr[1][0], expected[i])
                    stack.append(expr[1][1])
                elif expr[0] == 'case':
                    self.assertEqual(expr[1][0], expected[i])
                    stack.append(expr[1][1])
                elif expr[0] == 'default':
                    self.assertEqual(expr[0], expected[i])
                    stack.append(expr[1])
                elif expr[0] == 'randomvar':
                    self.assertEqual(expr[1][0], expected[i])
                    for subexpr in expr[1][1][::-1]:
                        stack.append(subexpr)
                else:
                    self.assertEqual(expr[0], expected[i])
                    for subexpr in expr[1][::-1]:
                        stack.append(subexpr)
                i += 1

    def test_reward_section(self):
        reward = self.rddl.domain.reward
        self.assertIsNotNone(reward)

    def test_action_preconditions_section(self):
        preconds = self.rddl.domain.preconds
        self.assertIsNotNone(preconds)
        self.assertEqual(len(preconds), 3)

    def test_state_action_constraints_section(self):
        constraints = self.rddl.domain.constraints
        self.assertIsNotNone(constraints)
        self.assertEqual(len(constraints), 24)

    def test_state_invariants_section(self):
        invariants = self.rddl.domain.invariants
        self.assertIsNotNone(invariants)
        self.assertEqual(len(invariants), 5)

    def test_instance_block(self):
        instance = self.rddl.instance
        self.assertIsInstance(instance, Instance)
        self.assertEqual(instance.name, 'inst_reservoir_res8')
        self.assertEqual(instance.domain, 'reservoir')
        self.assertEqual(instance.non_fluents, 'res8')
        self.assertEqual(instance.max_nondef_actions, 'pos-inf')
        self.assertEqual(instance.horizon, 40)
        self.assertAlmostEqual(instance.discount, 0.9)

    def test_instance_init_state_section(self):
        init_state = self.rddl.instance.init_state
        expected = [
            (('rlevel', ['t1']), 75.0),
            (('rlevel', ['t1', 't2']), -75),
            (('location', ['x']), 1.0),
            (('location', ['y']), 2),
            (('xPos', None), 0.0),
            (('yPos', None), 0.0),
            (('time', None), 0.0),
            (('picTaken', ['p1']), True),
            (('picTaken', ['p3']), False)
        ]
        self.assertEqual(init_state, expected)

    def test_nonfluents_block(self):
        non_fluents = self.rddl.non_fluents
        self.assertIsInstance(non_fluents, NonFluents)
        self.assertEqual(non_fluents.name, 'res8')
        self.assertEqual(non_fluents.domain, 'reservoir')

    def test_nonfluents_objects_section(self):
        objects = self.rddl.non_fluents.objects
        expected = [
            ('res', ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']),
            ('dim', ['x', 'y']),
            ('picture-point', ['p1', 'p2', 'p3'])
        ]
        self.assertListEqual(objects, expected)

    def test_nonfluents_initialization_section(self):
        init_non_fluent = self.rddl.non_fluents.init_non_fluent
        expected = [
            (('MAX_TIME', None), 12),
            (('MOVE_VARIANCE_MULT', None), 1e-05),
            (('RAIN_SHAPE', ['t1']), 0.0),
            (('RAIN_SCALE', ['t2', 't2']), 5.0),
            (('RAIN_SCALE', ['t7']), 25.0),
            (('RAIN_SHAPE', ['t8', 't7']), 1.0),
            (('RAIN_SCALE', ['t8']), 30.0),
            (('MAX_RES_CAP', ['t3']), 200.0),
            (('UPPER_BOUND', ['t3', 't5']), -180.0),
            (('MAX_RES_CAP', ['t4']), 300.2),
            (('DOWNSTREAM', ['t1', 't6']), True),
            (('DOWNSTREAM', ['t2', 't3']), True),
            (('DOWNSTREAM', ['t3', 't5']), True),
            (('DOWNSTREAM', ['t4', 't8']), True),
            (('DOWNSTREAM', ['t5', 't7']), True),
            (('DOWNSTREAM', ['t6', 't7']), True),
            (('DOWNSTREAM', ['t7', 't8']), True),
            (('SINK_RES', ['t8']), True)
        ]
        self.assertListEqual(init_non_fluent, expected)
