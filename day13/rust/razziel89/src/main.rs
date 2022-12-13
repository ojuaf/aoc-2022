#![feature(let_chains)]
// Expected input file names.
const SAMPLE1: &str = "sample.dat";
const REAL: &str = "stage_1.dat";

// Dependencies.
extern crate derive_more;
mod data;
mod io;

// tag::main[]
use anyhow::{Error, Result};
// Constants.

fn solve(file: &str) -> Result<()> {
    eprintln!("PROCESSING {}", file);

    // Read file and convert into data.
    let pairs = io::parse_chunks_to_data::<data::Input>(
        io::read_lines_from_file(file, 3)?,
        "package",
        None,
        None,
    )?;

    // Part 1.
    let ordered_correctly = pairs
        .iter()
        .enumerate()
        .filter_map(|(idx, el)| {
            if el.is_ordered_correctly() {
                Some(idx + 1)
            } else {
                None
            }
        })
        .sum::<usize>();

    println!("correctly ordered: {}", ordered_correctly);

    // Part 2.
    // Create divider packages. We wrote a parser so we might as well use it for easy creation of
    // the divider packages.
    let div1 = "[[2]]".parse::<data::Pkg>()?;
    let div2 = "[[6]]".parse::<data::Pkg>()?;

    // A value of "true" means this package is a marker.
    let mut all_pkgs = vec![(true, &div1), (true, &div2)];
    all_pkgs.extend(
        pairs
            .iter()
            .map(|el| vec![(false, &el.left), (false, &el.right)].into_iter())
            .flatten(),
    );

    // Sort using the comparison method created for part 1.
    all_pkgs.sort_by(|(_marker1, pkg1), (_marker2, pkg2)| pkg1.compare(pkg2).as_ordering());

    let (key_idx1, _) = all_pkgs
        .iter()
        .enumerate()
        .find(|(_idx, (marker, _pkg))| *marker)
        .ok_or(Error::msg("cannot find first marker"))?;

    let (key_idx2, _) = all_pkgs
        .iter()
        .enumerate()
        .find(|(idx, (marker, _pkg))| *marker && *idx != key_idx1)
        .ok_or(Error::msg("cannot find second marker"))?;

    println!("decoder key is {}", (key_idx1 + 1) * (key_idx2 + 1));

    Ok(())
}

fn main() -> Result<()> {
    solve(SAMPLE1)?;
    solve(REAL)?;

    Ok(())
}
// end::main[]
