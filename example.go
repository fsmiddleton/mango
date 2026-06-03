import (   
	"github.com/kuleuven/iron"
	"github.com/kuleuven/iron/api"
)

func example() error {
    var env iron.Env

    err := env.LoadFromFile(".irods/irods_environment.json")
    if err != nil {
        return err
    }

    env.Password = "my_password"

    ctx := context.Background()

    client, err := iron.New(ctx, env, iron.Option{
        ClientName:        "iron",
        Admin:             false, // Set to true to do all operations as admin, bypassing any ACLs
        MaxConns:          5,
    })
    if err != nil {
        return err
    }

    defer client.Close()

    objects, err := client.ListDataObjectsInCollection(ctx, "/path/to/data")
    if err != nil {
        return err
    }

    for _, object := range objects {
        fmt.Println(object.Path)
    }

    // Recursive walk through the tree, displaying access and metadata
    fn := func(path string, info api.Record, err error) error {
        if err != nil {
            return nil
        }

        fmt.Println(path)
        fmt.Printf("%v", info.Access())
        fmt.Printf("%v", info.Metadata())

        return nil
    }

    return client.Walk(ctx, "/path/to/more/data", fn, api.FetchAccess, api.FetchMetadata)
}