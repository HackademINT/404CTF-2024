use {
    anyhow::{anyhow, Result},
    env_logger,
    log::{debug, info},
    std::{env::args, fs::File, io::Read, process::exit}
};

const MASKS: &[u8] = &[
    0b10000000,
    0b01000000,
    0b00100000,
    0b00010000,
    0b00001000,
    0b00000100,
    0b00000010,
    0b00000001,
];

fn reverse_bits(byte: &mut u8) {
    for i in 0..4 {
        *byte ^= (*byte & MASKS[i]) >> 7-2*i;
        *byte ^= (*byte & MASKS[7-i]) << 7-2*i;
        *byte ^= (*byte & MASKS[i]) >> 7-2*i;
    }
}

fn try_byte_from_bits(bits: &[bool]) -> Result<u8> {
    if bits.len() != 8 {
        return Err(anyhow!("Cannot build byte from bit slice len != 8 (got {})", bits.len()));
    }
    let mut res: u8 = 0;
    for i in 0..8 {
        res ^= (bits[i] as u8) << 7-i;
    }
    Ok(res)
}

fn uart_unwrap(bytes: &[u8]) -> Result<Vec<u8>> {
    let bits = bytes
        .iter()
        .flat_map(|byte| {
            vec![
                byte & MASKS[0] == MASKS[0],
                byte & MASKS[1] == MASKS[1],
                byte & MASKS[2] == MASKS[2],
                byte & MASKS[3] == MASKS[3],
                byte & MASKS[4] == MASKS[4],
                byte & MASKS[5] == MASKS[5],
                byte & MASKS[6] == MASKS[6],
                byte & MASKS[7] == MASKS[7],
            ]
        })
        .collect::<Vec<bool>>();

    bits
        .chunks_exact(10)
        .map(|bits| try_byte_from_bits(&bits[1..9]))
        .collect::<Result<Vec<u8>>>()
}

fn main() -> Result<()> {
    env_logger::init();

    let mut args = args();
    if args.len() != 2 {
        println!("Wrong number of arguments ! \nUsage : ./solver [chall_file_path]\n\nExiting...");
        exit(1);
    }

    let chall_file_path = args.nth(1).expect("input file path smh not found in args");
    info!("Input path : \"{}\"", chall_file_path);


    let mut chall_file = File::open(chall_file_path)?;
    let mut chall: Vec<u8> = Vec::new();
    let _ = chall_file.read_to_end(&mut chall);
    debug!("File content :");
    chall.iter()
        .enumerate()
        .for_each(|(i, byte)| debug!("    Byte {i:02} : 0b{byte:08b}"));

    let mut unwrapped_chall = uart_unwrap(&chall)?;

    debug!("After uart_unwrap : ");
    unwrapped_chall.iter()
        .enumerate()
        .for_each(|(i, byte)| debug!("    Byte {i:02} : 0b{byte:08b}"));

    for byte in unwrapped_chall.as_mut_slice() {
        reverse_bits(byte);
        *byte = *byte & 0b01111111;
    }

    debug!("After bit reverse and parity bit masking : ");
    unwrapped_chall.iter()
        .enumerate()
        .for_each(|(i, byte)| debug!("    Byte {i:02} : 0b{byte:08b}"));

    println!("Flag : {}", String::from_utf8(unwrapped_chall)?);

    Ok(())
}
