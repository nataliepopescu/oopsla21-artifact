extern crate age;
use age::{x25519, Decryptor, Encryptor};
use std::time::SystemTime;
use std::time::Duration;
use std::io::Write as IoWrite;
use std::io::{self, Read, Write};
use std::iter;

fn now() -> SystemTime {
    return SystemTime::now();
}

fn elapsed(start: SystemTime) -> (Duration, bool) {
    match start.elapsed() {
        Ok(delta) => return (delta, false),
        _ => return (Duration::new(0, 0), true),
    }
}

const KB: usize = 1024;

// test size
fn bench_test_encrypt(n_iter: usize, recipient: x25519::Recipient, buf: &mut Vec<u8>, size: usize) {
    for _ in 0..n_iter {
        let mut output = Encryptor::with_recipients(vec![Box::new(recipient.clone())])
            .wrap_output(io::sink())
            .unwrap();
        output.write_all(&buf[..size]).unwrap();
        output.finish().unwrap();
    }
}

fn bench_test(n_iter: usize, identity: x25519::Identity, encrypted: &mut Vec<u8>, buf: &mut Vec<u8>, size: usize) {
    for _ in 0..n_iter {
        let decryptor = match Decryptor::new(&encrypted[..]).unwrap() {
            Decryptor::Recipients(decryptor) => decryptor,
            _ => panic!(),
        };
        let mut input = decryptor
            .decrypt(iter::once(&identity as &dyn age::Identity))
            .unwrap();
        input.read_exact(&mut buf[..size]).unwrap();
    }
}


#[no_mangle]
#[inline(never)]
fn bench() {
    // setup
    let identity = x25519::Identity::generate();
    let recipient = identity.to_public();
    let mut buf = vec![0u8; 1024 * KB];
    let size = 64 * KB;
    
    let mut encrypted = vec![];
    let mut output = Encryptor::with_recipients(vec![Box::new(recipient.clone())])
        .wrap_output(&mut encrypted)
        .unwrap();
    output.write_all(&buf[..size]).unwrap();
    output.finish().unwrap();

    let start = now();
    let mut timing_error: bool = false;
    let n_iterations: usize = 10;

    // bench
    //bench_test(n_iterations, &recipient, &mut buf, size);
    bench_test(n_iterations, identity, &mut encrypted, &mut buf, size);

    let (total, err) = elapsed(start);
    if err {
        timing_error = true;
    }

    if timing_error {
        let _r = writeln!(&mut io::stderr(), "{:}", "Timing error");
    } else {
        writeln!(&mut io::stderr(), "{:} {:} {:}.{:09}",
        n_iterations as u64,
        "Iterations; Time",
        total.as_secs(),
        total.subsec_nanos());
    }
}

fn main() {
    bench();
}
