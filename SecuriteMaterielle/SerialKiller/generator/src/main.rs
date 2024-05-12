use {
    anyhow::{anyhow, Result},
    env_logger,
    log::{debug, info},
    std::{env::args, fs::File, io::Write, process::exit}
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

fn parity_bit(byte: u8) -> u8 {
    (u8::count_ones(byte) % 2).try_into().unwrap() // pair = 0, impair = 1
}

fn try_byte_from_bits(bits: &[bool]) -> Result<u8> {
    if bits.len() != 8 {
        return Err(anyhow!("Cannot build byte from bit slice len != 8"));
    }
    let mut res: u8 = 0;
    for i in 0..8 {
        res ^= (bits[i] as u8) << 7-i;
    }
    Ok(res)
}

fn uart_wrap(bytes: &[u8]) -> Result<Vec<u8>> {
    let mut bits = bytes
        .iter()
        .flat_map(|byte| {
            vec![
                false,
                byte & MASKS[0] == MASKS[0],
                byte & MASKS[1] == MASKS[1],
                byte & MASKS[2] == MASKS[2],
                byte & MASKS[3] == MASKS[3],
                byte & MASKS[4] == MASKS[4],
                byte & MASKS[5] == MASKS[5],
                byte & MASKS[6] == MASKS[6],
                byte & MASKS[7] == MASKS[7],
                true,
            ]
        })
        .collect::<Vec<bool>>();

    let to_pad = bits.len() % 8;
    if to_pad != 0 {
        bits.append(&mut vec![true; 8-to_pad]);
    }

    bits
        .chunks_exact(8)
        .map(|bits| try_byte_from_bits(bits))
        .collect::<Result<Vec<u8>>>()
}

fn main() -> Result<()> {
    env_logger::init();

    let mut args = args();
    if args.len() != 3 {
        println!("Wrong number of arguments ! \nUsage : ./generator [flag] [output_file_path]\n\nExiting...");
        exit(1);
    }

    let flag_str = args.nth(1).expect("flag smh not found");
    if !flag_str.is_ascii() {
        return Err(anyhow!("String must only contain ascii chars"));
    }
    info!("Flag : \"{}\"", flag_str);
    let mut flag = flag_str.into_bytes();

    let out_file_path = args.next().expect("output file path smh not found");
    info!("Output path : \"{}\"", out_file_path);

    debug!("flag bits : ");
    flag.iter()
        .enumerate()
        .for_each(|(i, byte)| debug!("    Byte {i:02} : 0b{byte:08b}"));

    for byte in flag.as_mut_slice() {
        reverse_bits(byte);
        *byte = *byte | parity_bit(*byte);
    }

    debug!("After bit reverse and parity bit : ");
    flag.iter()
        .enumerate()
        .for_each(|(i, byte)| debug!("    Byte {i:02} : 0b{byte:08b}"));

    let transformed_flag = uart_wrap(&flag)?;

    debug!("After uart_wrap : ");
    transformed_flag.iter()
        .enumerate()
        .for_each(|(i, byte)| debug!("    Byte {i:02} : 0b{byte:08b}"));

    let mut out_file = File::create(out_file_path)?;
    let _ = out_file.write_all(&transformed_flag);

    println!("Write successful !");
    Ok(())
}
