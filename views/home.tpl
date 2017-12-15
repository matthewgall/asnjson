% include('global/header.tpl', title='Turning BGP... to JSON')
<div class="container">
    <div class="starter-template">
        <h1>Welcome to asnjson</h1>
        <p class="lead">
            Need ASN information in an application accessible method? <br />
            If you need this, then asnjson.com is for you!
        </p>
        <p>&nbsp;</p>
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h2 class="panel-title">Lookup an address</h3>
            </div>
            <div class="panel-body">
                <form class="form-inline" method="POST" action="/">
                    <fieldset>
                        <div class="form-group">
                            <input type="text" name="address" class="form-control" id="address"
                                placeholder="8.8.8.8">
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">Lookup</button>
                        </div>
                    </fieldset>
                </form>
            </div>
        </div>
    </div>
</div>
% include('global/footer.tpl')