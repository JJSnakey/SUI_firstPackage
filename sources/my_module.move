/*
Joshua Greer
From SUI tutorial
"Your First SUI App"

also testing new kali vm and term

important commands:
sui move build
sui move test
*/

module my_first_package::my_module {

    // Part 1: Imports===============================================================================================================
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    // Part 2: Struct definitions============================================================================================
    public struct Sword has key, store {
        id: UID,
        magic: u64,
        strength: u64,
    }

    public struct Forge has key, store {
        id: UID,
        swords_created: u64,
    }

    // Part 3: Module initializer to be executed when this module is published======================================================================
    fun init(ctx: &mut TxContext) {
        let admin = Forge {
            id: object::new(ctx),
            swords_created: 0,
        };
        // Transfer the forge object to the module/package publisher
        transfer::public_transfer(admin, tx_context::sender(ctx));
    }

    // Part 4: Accessors required to read the struct attributes======================================================================
    public fun magic(self: &Sword): u64 {
        self.magic
    }

    public fun strength(self: &Sword): u64 {
        self.strength
    }

    public fun swords_created(self: &Forge): u64 {
        self.swords_created
    }

    // Part 5: Public/entry functions (introduced later in the tutorial)======================================================================

    public fun sword_create(magic: u64, strength: u64, recipient: address, ctx: &mut TxContext) {

        //part2
        // create a sword
        let sword = Sword {
            id: object::new(ctx),
            magic: magic,
            strength: strength,
        };
        // transfer the sword
        transfer::transfer(sword, recipient);

    }

    public fun sword_transfer(sword: Sword, recipient: address, _ctx: &mut TxContext) {

        // transfer the sword
        transfer::public_transfer(sword, recipient);
        
    }

    //part3
    /// Constructor for creating swords
    public fun new_sword(
        forge: &mut Forge,
        magic: u64,
        strength: u64,
        ctx: &mut TxContext,
    ): Sword {
        forge.swords_created = forge.swords_created + 1;
        Sword {
            id: object::new(ctx),
            magic: magic,
            strength: strength,
        }
    }

    // Part 6: Private functions (if any)==============================================================================================
    
    //tests (from tutorial)
    
    //part2
     #[test]
    fun test_sword_transactions() {
        use sui::test_scenario;

        // create test addresses representing users
        let admin = @0xBABE;
        let initial_owner = @0xCAFE;
        let final_owner = @0xFACE;

        // first transaction to emulate module initialization
        let mut scenario_val = test_scenario::begin(admin);
        let scenario = &mut scenario_val;
        {
            init(test_scenario::ctx(scenario));
        };
        // second transaction executed by admin to create the sword
        test_scenario::next_tx(scenario, admin);
        {
            // create the sword and transfer it to the initial owner
            sword_create(42, 7, initial_owner, test_scenario::ctx(scenario));
        };
        // third transaction executed by the initial sword owner
        test_scenario::next_tx(scenario, initial_owner);
        {
            // extract the sword owned by the initial owner
            let sword = test_scenario::take_from_sender<Sword>(scenario);
            // transfer the sword to the final owner
            sword_transfer(sword, final_owner, test_scenario::ctx(scenario))
        };
        // fourth transaction executed by the final sword owner
        test_scenario::next_tx(scenario, final_owner);
        {
            // extract the sword owned by the final owner
            let sword = test_scenario::take_from_sender<Sword>(scenario);
            // verify that the sword has expected properties
            assert!(magic(&sword) == 42 && strength(&sword) == 7, 1);
            // return the sword to the object pool
            test_scenario::return_to_sender(scenario, sword)
            // or uncomment the line below to destroy the sword instead
            // test_utils::destroy(sword)
        };
        test_scenario::end(scenario_val);
    }

    //part1
    #[test]
    public fun test_sword_create() {

        use sui::transfer;
        
        // Create a dummy TxContext for testing
        let mut ctx = tx_context::dummy();

        // Create a sword
        let sword = Sword {
            id: object::new(&mut ctx),
            magic: 42,
            strength: 7,
        };

        // Check if accessor functions return correct values
        assert!(magic(&sword) == 42 && strength(&sword) == 7, 1);

        // Create a dummy address and transfer the sword
        let dummy_address = @0xCAFE;
        transfer::transfer(sword, dummy_address);

    }

    //part3
    #[test_only] use sui::test_scenario as ts;

    #[test_only] const ADMIN: address = @0xAD;

    #[test]
    public fun test_module_init() {
        let mut ts = ts::begin(@0x0);

        // first transaction to emulate module initialization.
        {
            ts::next_tx(&mut ts, ADMIN);
            init(ts::ctx(&mut ts));
        };

        // second transaction to check if the forge has been created
        // and has initial value of zero swords created
        {
            ts::next_tx(&mut ts, ADMIN);

            // extract the Forge object
            let forge: Forge = ts::take_from_sender(&mut ts);

            // verify number of created swords
            assert!(swords_created(&forge) == 0, 1);

            // return the Forge object to the object pool
            ts::return_to_sender(&mut ts, forge);
        };

        ts::end(ts);
    }

}