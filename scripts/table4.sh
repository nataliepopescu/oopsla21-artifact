BMARK_DIRS=("tantivy" "rage" "swc" "warp" "iron" "RustPython" "zola" "COST")
BIN_NAMES=("test_bc" "test_bc" "test_bc" "hello" "hello" "test_bc" "zola" "test_bc")

script_path=`realpath $0`
SCRIPT_ROOT=`dirname $script_path`/
ROOT=`dirname $script_path`/../benchmarks

function patch_bmark {
    BMARK=$1
    # revert to original
    cd $ROOT/$BMARK
    cp $ROOT/patch/$BMARK.Cargo.lock Cargo.lock
    cp $ROOT/patch/$BMARK.Cargo.toml Cargo.toml
    if [ "$BMARK" == "tantivy" ] || [ "$BMARK" == "swc" ] || [ "$BMARK" == "RustPython" ]; then
        mkdir -p bin
        cp $ROOT/patch/$BMARK.test_bc.rs bin/test_bc.rs
    fi

    if [ "$BMARK" == "COST" ]; then
        cp $ROOT/patch/$BMARK.pagerank.rs src/bin/pagerank.rs
        cp $ROOT/patch/$BMARK.lib.rs src/lib.rs
        cp $ROOT/patch/$BMARK.bench.rs src/bench.rs
    fi


    if [ "$BMARK" == "rage" ]; then
        mkdir -p age/bin
        cp $ROOT/patch/age.Cargo.toml age/Cargo.toml
        cp $ROOT/patch/age.test_bc.rs age/bin/test_bc.rs
    fi
}

function gen_binary {
    cd $ROOT

    BMARK_DIR=$1
    BIN_NAME=$2

    echo $BMARK_DIR $BIN_NAME
    cd $BMARK_DIR

    date > log

    #if [ ! -d "vendor-safe" ] 
    #then
    # Create vendor-unsafe and unsafe
    if [ "$BMARK_DIR" == "rage" ]; then
        cd age
    fi
    rm -rf vendor-safe vendor-unsafe vendor
    cargo vendor >> log 2>&1
    mv vendor vendor-safe
    cp -r vendor-safe vendor-unsafe
    if [ "$BMARK_DIR" == "rage" ]; then
        cd ..
    fi

    # Convert
    # echo "Converting unchecked indexing for $BMARK_DIR"
    if [ "$BMARK_DIR" == "rage" ]; then
        cd age
        # Copy the files 
        ln -sf $ROOT/../scripts/regexify.py .; ln -sf $ROOT/make_patch.py .
        rm -f vendor; ln -s vendor-safe vendor; python make_patch.py -t $(pwd)/.. -r age/vendor >> log 2>&1
    else 
        # Copy the files 
        ln -sf $ROOT/../scripts/regexify.py .; ln -sf $ROOT/make_patch.py .
        rm -f vendor; ln -s vendor-safe vendor; python make_patch.py -t $(pwd) -r vendor >> log 2>&1
    fi

    # Gen unsafe binary
    rm -f vendor; ln -s vendor-unsafe vendor

    if [ "$BMARK_DIR" == "iron" ]; then
        cd examples 
    fi
    RUSTFLAGS="-Awarnings -C codegen-units=1 -Cembed-bitcode=yes"  cargo rustc --bin $BIN_NAME --release --  -Clto=fat >> log 2>&1
    if [ "$BMARK_DIR" == "iron" ]; then
        cd ..
    fi
    if [ "$BMARK_DIR" == "rage" ]; then
        cd ..
    fi
    cp ./target/release/$BIN_NAME ${BIN_NAME}-unsafe
    
    # Gen safe binary
    if [ "$BMARK_DIR" == "rage" ]; then
        cd age
    fi
    rm -f vendor; ln -s vendor-safe vendor;

    if [ "$BMARK_DIR" == "iron" ]; then
        cd examples
    fi
    RUSTFLAGS="-Awarnings -C codegen-units=1 -Cembed-bitcode=yes"  cargo rustc --bin $BIN_NAME --release --  -Clto=fat  >> log 2>&1;
    if [ "$BMARK_DIR" == "iron" ]; then
        cd ..
    fi
    if [ "$BMARK_DIR" == "rage" ]; then
        cd ..
    fi
    cp ./target/release/$BIN_NAME ${BIN_NAME}-safe
    
    # diff
    if cmp -s -- ${BIN_NAME}-safe ${BIN_NAME}-unsafe; then
        echo $BMARK_DIR binaries are identical
    else
        echo $BMARK_DIR binaries are different
    fi
}

function gen_perf_diff {
    BMARK=$1
    BIN_NAME=$2

    if [ "$BMARK" == "tantivy" ] || [ "$BMARK" == "swc" ] || [ "$BMARK" == "RustPython" ]; then
        # run test_bc
        echo $BMARK
    fi
}

for i in "${!BMARK_DIRS[@]}"; do
    patch_bmark "${BMARK_DIRS[i]}"
    gen_binary "${BMARK_DIRS[i]}" "${BIN_NAMES[i]}"
done 

cd $SCRIPT_ROOT
python3 table4_run.py
wait

