% include('global/header.tpl', title=data['ip'])
<div class="container">
    <div class="starter-template">
        <div class="well well-lg">
            <h1>{{data['ip']}}</h1>
            <p id="counterVal" style="font-size: 42px;">
<pre>
ASN: {{data['asn']}}
Prefix: {{data['prefix']}}
Owner: {{data['owner']}}
Country: {{data['cc']}}
</pre>
            </p>
        </div>
        
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">Need to script it?</h3>
            </div>
            <div class="panel-body">
                <p>
                Verify the results using curl:
                </p>
                <pre>curl https://asnjson.com/{{data['ip']}}/json</pre>
            </div>
        </div>
        
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">Need to lookup something else?</h3>
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